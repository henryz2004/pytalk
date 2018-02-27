from pynet import socket_utility


class Message:
    """
    Stores a string message and whether or not it is a notification (NTF) or plain message (MSG)
    """

    def __init__(self, message):

        self.message = message

    def prepare(self, max_bytes=None):
        return socket_utility.prepare(self.message, max_bytes=max_bytes)

    def __repr__(self):
        return self.message
