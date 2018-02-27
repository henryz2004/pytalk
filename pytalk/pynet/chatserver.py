from pynet import serverbackend


# a bunch of remote methods the client could call
def assign_name(server, client, ip, alias_arg):
    """Remote event the client calls when it decides a name. Input alias into alias_arg"""

    # Update the entry for the client in server.client_info
    server.client_info[ip]["alias"] = alias_arg

    # notify the clients in the server that this dude has joined
    server.invoke_all("user_joined", ip, alias_arg, exception=client)


def typing(server, client, ip):

    # TODO: ip as argument or alias (or both?)
    server.invoke_all(
        "user_typing",
        ip,
        server.client_info[ip]["alias"],
        exception=client
    )


def stopped_typing(server, client, ip):

    # TODO: ip as argument or alias (or both?)
    server.invoke_all(
        "user_stopped_typing",
        ip,
        server.client_info[ip]["alias"],
        exception=client
    )


def send_message(server, client, ip, message):
    print(ip, "sent", message)
    server.invoke_all(
        "user_sent_message",
        ip,
        server.client_info[ip]["alias"],
        message
    )


def on_leave(server, client, ip):
    if server.client_info[ip]["alias"]:
        server.invoke_all("user_left", ip, server.client_info[ip]["alias"], exception=client)


def ping(server, client, ip):
    server.invoke(client, "pong")


if __name__ == "__main__":

    serverbackend.init_server(
        events={
            "assign_name"    : [1, assign_name],
            "typing"         : [0, typing],
            "stopped_typing" : [0, stopped_typing],
            "send_message"   : [1, send_message],
            "ping"           : [0, ping]
        },
        leave=on_leave
    )
