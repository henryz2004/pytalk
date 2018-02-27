def prepare(message, max_bytes=None):
    """
    Prepares a message for being sent through a socket. Unless otherwise
    specified, the maximum number of bytes that can be sent at once through
    a socket is 1024, and therefore the maximum length a message can be is
    1024-4 = 1020.

    Message architecture:
    [Length of message][Message]

    Examples:

    >>> prepare("Hello")
    b'5   Hello'

    >>> prepare("REQUEST_CLOSE")
    b'13  REQUEST_CLOSE'

    >>> prepare("Hi there", max_bytes=36)
    b'8   Hi there'

    >>> prepare("Very very very very very long message", max_bytes=36)
    Traceback (most recent call last):
    ...
    AssertionError: Message length exceeded 32
    """

    # Handle defaults
    if max_bytes is None:
        max_bytes = 1024

    message = str(message)
    msg_len = len(message)

    # assertions
    assert msg_len <= (max_bytes - 4), "Message length exceeded " + str(max_bytes - 4)
    
    return (str(msg_len).ljust(4) + message).encode()


def partition(message):
    """
    Takes in a decoded message (presumably passed through prepare()) and
    returns a list of all contained messages. The messages are strings

    Example:

    >>> partition("5   Hello6   World!")
    ['Hello', 'World!']
    """

    messages = []

    while len(message) > 0:

        prefix = message[:4].strip()

        try:
            msg_len = int(prefix)

        except ValueError:
            print("Erroneous message prefix:", prefix)

            msg_len = len(message)              # assume that all that's left is this message

        messages.append(message[4:4+msg_len])   # add message
        message = message[4+msg_len:]           # slice past current message to next message

    return messages


if __name__ == "__main__":

    print(prepare("Hello"))
    print(prepare("REQUEST_CLOSE"))
    print(prepare("Hi there", max_bytes=36))
    print(partition("5   Hello6   World!"))
