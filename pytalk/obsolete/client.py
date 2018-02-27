# https://www.tutorialspoint.com/python/python_networking.htm

import socket
import time

class Client:

    def __init__(self, port, host=None):

        self.s = socket.socket()

        self.host = socket.gethostname() if host == None else host
        self.port = port

        self.s.connect((self.host, self.port))

        self.to_send = []       # messages to send, will be sent during each 'cycle'


    def send(self, message):

        # When sending a message also send length of it (first 3 bytes will always be allocated to this)
        # this way if multiple messages are sent through one real message then we can figure out the
        # start and end of all 3 messages

        message_length = len(message)

        # first assert that the length of message is less than 1022
        if message_length > 1021:
            print("Message could not be sent because it is too long")

            return "ERR_LEN"    # Error length

        # message length should be at most 4 bytes long, so do that
        prefix = str(message_length).ljust(4)

        # add prefix to message and send it
        modified_message = prefix + message

        self.s.send(modified_message.encode())

        return "SUCCESS"


    def check_command(self, message):
        """Checks for special server to client commands (i.e. shutdown). Should be called before other methods"""

        if message == "SCC_CLS":
            self.s.close()

            print("Connection closed")


    def close(self):

        # send message to server requesting to close the socket
        self.send("REQUEST_LEAVE")

        # this is bad
        close_confirmation = self.s.recv(1024).decode("utf-8")
        self.check_command(close_confirmation)


    def shutdown(self):

        self.send("REQUEST_SHUTDOWN")
    
        # this is bad
        close_confirmation = self.s.recv(1024).decode("utf-8")
        self.check_command(close_confirmation)
        

if __name__ == "__main__":
    
    client = Client(31415)
    client.send("Hi")
    client.send("How are you")
    client.shutdown()
