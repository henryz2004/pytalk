# https://www.tutorialspoint.com/python/python_networking.htm

import select
import socket

class Server:

    def __init__(self, port):

        self.s = socket.socket()
        
        self.host = socket.gethostname()
        self.port = port

        self.s.bind((self.host, self.port))

        self.alive = True       # not strictly necessary

        self.sockets = [self.s] # list of sockets that can potentially be read from
        self.clients = []       # list of clients


    def start(self, queue_limit):
        """Sever starts listening and accepting connections"""

        self.s.listen(queue_limit)

        # Constantly accept connections while self is still running
        while self.alive:

            # select availabe
            readable, writable, _ = select.select(self.sockets, [], [], 0) # nonblocking
            
            # loop through all readable sockets and read
            for index, r_socket in enumerate(readable):

                # if socket is server socket then accept connection
                if r_socket == self.s:

                    connection = self.s.accept()

                    print("New connection from", connection[1])

                    # add connection to clients and sockets
                    self.sockets.append(connection[0])
                    self.clients.append(connection[1])

                # otherwise receive client message, log message, and reply accordingly
                else:

                    msg = r_socket.recv(1024).decode("utf-8")

                    # split the messages
                    # we're going to need a better and more reliable message sending technique
                    messages = self.split_msg(msg)

                    # handle each message
                    for message in messages:

                        print(self.clients[index-1][0], "sent", message)

                        self.check_command(r_socket, message)
                    

        # close socket when done
        self.s.close()

        
    def send(self, client, message):

        client.send(message.encode(), )


    def split_msg(self, message_string):

        messages = []

        while len(message_string) > 0:

            # find the first 4 bytes of the string, strip whitespace, and try
            # to cast to int
            prefix = message_string[0:4]
            prefix.strip()

            try:
                msg_len = int(prefix)

            except Exception as e:

                print("Prefix", prefix, "is invalid")

                msg_len = len(message_string)   # no other choice

            message = message_string[4:4+msg_len]

            messages.append(message)

            message_string = message_string[4+msg_len:]

        return messages


    def check_command(self, client, message):

        if message == "REQUEST_SHUTDOWN":

            print("Shutting down server")

            self.shutdown()

        elif message == "REQUEST_LEAVE":

            print("Closing connection")

            self.close(client)


    def close(self, client):

        # send "SCC_CLS" to client to notify that they should now close the socket
        self.send(client, "SCC_CLS")    # Server-client command: close

        client.close()

        # find index of client in sockets and use that to remove from self.clients
        client_index = self.sockets.index(client)-1

        self.sockets.remove(client)
        self.clients.pop(client_index)


    def shutdown(self):
        """Shuts down server"""

        client_count = len(self.clients)

        for i in range(client_count):
            self.close(self.sockets[1])

        self.alive = False


if __name__ == "__main__":
    
    # Make a server
    server = Server(31415)
    server.start(5)
