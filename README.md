# pytalk
Chat Program developed entirely in Python and Kivy.

PyTalk is a simple and lightweight Kivy-based chat application that uses sockets. I made it Because I Can, and it is built on top of an event based homemade framework. It is easily expandable; you can add custom Remote Events or use the networking framework by itself for a completely different task.

To run, first run `chatserver.py` in the background. This will start a server that the client can connect to. Then, in a separate command prompt (or just run concurrently), run `clientgui.py`. After a bunch of omnious error-like startup messages from kivy, a window should come up (if there's a server to connect to). Enter your alias (a user system has not been set up yet) and then press continue. After that you have officially entered the chat room.

The host is assumed to be the local computer, but it is trivial and likely necessary to change it. Simply provide a `host` kwarg for `init_server()` and `init_client()` and you'll be good to go. The default port is `31415`, but that can also be changed.

Many optimizations can be made, such as:
  1. Removing the `Message` class
  2. No-loss message sending and receiving
  3. Implementing Blocking Remote Events
  4. Concurrent Server

If you wish you can always contribute! ^-^
Of course you can always just... take the files and leave but WHY WOULD YOU?

Please attribute this to Henry Zhang