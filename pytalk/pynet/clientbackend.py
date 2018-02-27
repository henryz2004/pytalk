# https://www.tutorialspoint.com/python/python_networking.htm

from pynet import message as msg_mod, socket_utility
import select
import socket
import threading


class Client:

    def __init__(self, port, host=None, events=None, abort=None):

        self.s = socket.socket()

        self.host = socket.gethostbyname(socket.gethostname()) if host is None else host
        self.port = port

        self.s.connect((self.host, self.port))

        self.alive = True
        self.abort = abort

        self.servers = [self.s] # to pass into select.select
        self.pending = []       # messages to send, will be sent during each 'cycle'. stores Messages

        # threading locks
        self.queue_lock = threading.Lock()  # queue of pending messages lock

        # remote event variables
        self.events = {} if events is None else events  # refer serverbackend.py
        self.event_id = None
        self.args = []
        self.arg_counter = -2   # counts arguments for remote events

    def initiate(self):
        """Returns big loop thread"""

        bigloop_thread = threading.Thread(target=self.mainloop)
        bigloop_thread.daemon = True

        return bigloop_thread

    def mainloop(self):
        """Big while loop that sends and recvs periodically"""

        # try-except to catch ConnectionResetError in case something happens
        try:

            while self.alive:

                # see if the server has sent anything
                readable, _, _ = select.select(self.servers, [], [], 0)

                # there's only going to be 1 server...
                for server in readable:

                    # read message and make sure it's not a command
                    message = server.recv(1024).decode("utf-8")

                    messages = socket_utility.partition(message)

                    # handle notifications
                    for ntf in messages:
                        shutdown = self.check_command(ntf.message)

                        if shutdown:
                            print("Received shutdown command")
                            break

                        # remote event handling
                        if ntf.message == "CALL_RE":
                            self.arg_counter = -1

                        elif ntf.message in self.events and self.arg_counter == -1:
                            self.arg_counter = 0
                            self.event_id = ntf.message

                        elif -1 < self.arg_counter < self.events[self.event_id][0]:
                            self.arg_counter += 1
                            self.args.append(ntf.message)

                        # call remote event if possible
                        # only default argument is self
                        if self.event_id and self.arg_counter >= self.events[self.event_id][0]:
                            self.events[self.event_id][1](
                                self,
                                *self.args
                            )
                            self.arg_counter = -2
                            self.event_id = None
                            self.args = []

                if self.alive:
                    # send a pending message - only 1 in order to avoid clustering
                    with self.queue_lock:
                        if len(self.pending) > 0:
                            self.send(self.pending.pop(0))

        except ConnectionResetError:
            if self.abort:
                self.abort(1)   # 1 = reset
            else:
                print("Connection forcibly reset by remote host")

        print("Mainloop exited")

    def send(self, message):
        self.s.send(message.prepare())

    def invoke(self, event_id, *args):
        self.queue("CALL_RE")
        self.queue(event_id)
        for arg in args:
            self.queue(arg)

    def queue(self, message):

        with self.queue_lock:
            self.pending.append(msg_mod.Message(message))

    def check_command(self, message):
        """Checks for special server to client commands (i.e. shutdown). Should be called before other methods"""

        if message == "SCC_CLS":
            self.s.close()
            self.alive = False

            print("Connection closed")
            return True
        
        return False

    def close(self):
        self.queue("REQUEST_LEAVE")

    def shutdown(self):
        self.queue("REQUEST_SHUTDOWN")


def init_client(**kwargs):

    client = Client(31415, **kwargs)
    return client, client.initiate()


if __name__ == "__main__":
    
    c, thread = init_client()
    thread.start()
    thread.join()
