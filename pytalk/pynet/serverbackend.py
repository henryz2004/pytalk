# https://www.tutorialspoint.com/python/python_networking.htm
# What's new? Messages have been completely deprecated. Max message
# length is now 1020
# TODO: Message end flag

import select
import socket
from pynet import socket_utility


class Server:

    def __init__(self, port, host=None, events=None, join=None, leave=None, abort=None):

        self.s = socket.socket()
        
        self.host = socket.gethostbyname(socket.gethostname()) if host is None else host
        self.port = port

        self.s.bind((self.host, self.port))

        self.alive = True           # not strictly necessary
        self.join = join
        self.leave = leave
        self.abort = abort

        self.sockets = [self.s]     # list of sockets that can potentially be read from
        self.clients = []           # list of clients (ip, port)
        self.client_info = {}       # ip address and associated data    (dict of dict)

        self.events = {} if events is None else events  # key: event_id, value: [arg_count, function]

    def start(self, queue_limit):
        """Sever starts listening and accepting connections"""

        self.s.listen(queue_limit)

        try:
            # Constantly accept connections while self is still running
            while self.alive:

                # select available
                readable, _, _ = select.select(self.sockets, [], [], 0)

                # loop through all readable sockets and read
                for r_socket in readable:

                    # because self.alive is volatile in the sense that it could change,
                    # stop dealing with clients if the server isn't even alive anymore
                    if not self.alive:
                        break

                    # if socket is server socket then accept connection
                    if r_socket == self.s:

                        connection = self.s.accept()

                        print("New connection from", connection[1])

                        # add connection to clients and sockets
                        self.sockets.append(connection[0])
                        self.clients.append(connection[1])

                        # default only keeps track of remote event calling
                        self.client_info[connection[1][0]] = {"alias": None, "fun": {"i": -2, "id": None, "args": []}}

                        # call self.join if bound
                        if self.join:
                            self.join(self, connection[0], connection[1][0])     # pass in server, socket, and ip

                    # otherwise receive client message, log message, and reply accordingly
                    else:

                        msg = r_socket.recv(1024).decode("utf-8")
                        ip = self.clients[self.sockets.index(r_socket)-1][0]

                        messages = socket_utility.partition(msg)

                        # handle notifications
                        for ntf in messages:
                            command = self.check_command(r_socket, ntf)

                            if command:
                                break   # stop dealing with this client

                            # check to see if client is calling remote function/event
                            # signal - next notification will be event_id
                            if ntf == "CALL_RE":
                                print("[ RE ] Received event invocation")
                                self.client_info[ip]["fun"]["i"] = -1

                            elif ntf in self.events and self.client_info[ip]["fun"]["i"] == -1:
                                print("[ RE ] Identified event_id as", ntf)
                                self.client_info[ip]["fun"]["i"] = 0
                                self.client_info[ip]["fun"]["id"] = ntf

                            elif -1 < self.client_info[ip]["fun"]["i"] < self.events[self.client_info[ip]["fun"]["id"]][0]:
                                print("[ RE ] Received", ntf, "as argument for", self.client_info[ip]["fun"]["id"])
                                self.client_info[ip]["fun"]["i"] += 1
                                self.client_info[ip]["fun"]["args"].append(ntf)

                            # call remote event if possible
                            # pass in the 3 necessary arguments (server, client, ip) + any other args

                            if self.client_info[ip]["fun"]["id"] and self.client_info[ip]["fun"]["i"] >= self.events[self.client_info[ip]["fun"]["id"]][0]:
                                print("[ RE ] Delegating event", self.client_info[ip]["fun"]["id"], "with arguments", self.client_info[ip]["fun"]["args"])
                                self.events[self.client_info[ip]["fun"]["id"]][1](
                                    self,
                                    r_socket,
                                    ip,
                                    *self.client_info[ip]["fun"]["args"]
                                )
                                # reset vars
                                self.client_info[ip]["fun"] = {"i": -2, "id": None, "args": []}

        except ConnectionResetError:
            if self.abort:
                self.abort(1)
            else:
                print("Connection was forcibly reset by remote host")

        finally:
            # close socket when done
            self.s.close()

    def send(self, client, message):
        client.send(socket_utility.prepare(message))

    def invoke(self, client, event_id, *args):
        self.send(client, "CALL_RE")
        self.send(client, event_id)
        for arg in args:
            self.send(client, arg)

    def invoke_all(self, event_id, *args, exception=None):
        print("[ RE ] Invoking", event_id, "with arguments", args)
        for client in self.sockets[1:]:
            if client == exception:
                continue

            self.invoke(client, event_id, *args)

    def broadcast(self, message, exception=None):
        for client in self.sockets[1:]:
            if client == exception:
                continue

            self.send(client, message)

    def check_command(self, client, message):

        if message == "REQUEST_SHUTDOWN":
            print("Shutting down server")

            self.shutdown()
            return True

        elif message == "REQUEST_LEAVE":
            print("Closing connection")

            self.close(client)
            return True

        return False

    def close(self, client):

        # send "SCC_CLS" to client to notify that they should now close the socket
        self.send(client, "SCC_CLS")  # Server-client command: close

        # find index of client in sockets and use that to remove from self.clients
        client_index = self.sockets.index(client) - 1
        ip = self.clients[client_index][0]

        # call self.leave if bound
        if self.leave:
            self.leave(self, client, ip)

        self.sockets.remove(client)
        self.clients.pop(client_index)

        client.close()

        del self.client_info[ip]

    def shutdown(self):
        """Shuts down server"""

        self.broadcast("SCC_CLS")
        self.alive = False


def init_server(**kwargs):

    # Find host
    host = socket.gethostbyname(socket.gethostname())

    print(host)

    # Make a server
    server = Server(31415, host=host, **kwargs)
    server.start(5)

    return server


if __name__ == "__main__":

    init_server()
