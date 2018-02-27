# TODO: Self-update

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from pynet import clientbackend as client_srvc
import time

Window.clearcolor = (1, 1, 1, 1)


class TextMessage(Label):
    pass


class President(ScreenManager):

    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__(**kwargs)
        self.clients_currently_typing = set()

    def on_clients_currently_typing(self):
        print("clients_currently_typing updated")

        # re-render curr_typing
        curr_typing = ""

        for typing_client in self.clients_currently_typing:
            curr_typing += typing_client + ", "

        if curr_typing == "":
            self.ids.curr_typing.text = ""
        else:
            self.ids.curr_typing.text = curr_typing[:-2] + " typing..."

    def name_update(self, val):
        if val.strip() == "":
            self.ids.continue_button.disabled = True
        else:
            self.ids.continue_button.disabled = False

    def continue_as(self, name):
        # make sure name isn't empty
        if name.strip() == "":
            return

        client.invoke("assign_name", name)              # TODO: Better mechanics

        self.current = "chatscreen"

    def send_message(self, message):
        global client

        # make sure the message isn't empty
        if message.strip() == "":
            return

        client.invoke("send_message", message)  # client.queue(message)

        self.ids.msg_in.text = ""
        self.ids.msg_in.focus = True    # fixme

    def make_message(self, message, markup=None):
        if markup is None: markup = False
        text = TextMessage(markup=markup, text=message)
        self.ids.msg_grid.add_widget(text)
        self.ids.msg_scroll.scroll_to(text)

    def recv_message(self, sender, message):
        self.make_message("[b]" + sender + "[/b]" + " : " + message, markup=True)

    def start_typing(self, text):
        if self.current == "namescreen":
            return
        if len(text) == 0:
            client.invoke("stopped_typing")
        else:
            client.invoke("typing")


class LayoutTest(App):

    def build(self):
        global manager, client

        manager = President()
        Clock.schedule_interval(lambda dt: pong(client), 1/3)
        return manager

    def on_stop(self):
        global client, thread

        # join the thread and close the client
        client.close()
        thread.join()


# remote events the server could invoke
def user_joined(client, ip, alias):
    print(alias, "has joined the room")
    if manager.current == "chatscreen":
        manager.make_message("[i]" + alias + " has joined the room[/i]", markup=True)


def user_left(client, ip, alias):
    print(alias, "has left the room")
    manager.make_message("[i]" + alias + " has left the room[/i]", markup=True)


def user_typing(client, ip, alias):
    manager.clients_currently_typing.add(alias)
    manager.on_clients_currently_typing()


def user_stopped_typing(client, ip, alias):
    manager.clients_currently_typing.discard(alias)
    manager.on_clients_currently_typing()


def user_sent_message(client, ip, alias, message):
    manager.recv_message(alias, message)


def abort(err_code):
    print("[ ** ] Connection aborted; errno", err_code)

    if err_code == 1:
        print("[ ** ] Connection forcibly reset by remote host")
        manager.make_message("[i]You have been disconnected from the server[/i]", markup=True)


def pong(client):
    if pong.ponged:
        time = millis()
        diff = time - pong.time
        manager.ids.ping.text = str(diff) + " ms"
        pong.time = millis()
        pong.ponged = False
    else:
        pong.ponged = True
        pong.time = millis()
        client.invoke("ping")


def millis():
    return int(round(time.time() * 1000))


if __name__ == '__main__':

    pong.ponged = False
    client, thread = client_srvc.init_client(
        events={
            "user_joined"         : (2, user_joined),
            "user_left"           : (2, user_left),
            "user_typing"         : (2, user_typing),
            "user_stopped_typing" : (2, user_stopped_typing),
            "user_sent_message"   : (3, user_sent_message),
            "pong"                : (0, pong)
        },
        abort=abort
    )
    thread.start()

    LayoutTest().run()
