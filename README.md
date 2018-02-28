# PyTalk
Chat Program developed entirely in Python and Kivy.

PyTalk is a simple and lightweight Kivy-based chat application that uses sockets.

This is built on top of a client-server framework [`PyNet`](https://github.com/henryz2004/pynet), which is also made by me. The chat application is easily expandable; you can add custom Remote Events and functionality by expanding on the main client and server script. The only 2 non-standard-library dependencies this requires is PyNet and Kivy, which can be easily installed using `pip`.

To run, first run `chatserver.py` in the background. This will start a server that the client can connect to. Then, in a separate command prompt (or just run concurrently), run `clientgui.py`. After a bunch of omnious error-like startup messages from kivy, a window should come up (if there's a server to connect to). Enter your alias (a user system has not been set up yet) and then press continue. After that you have officially entered the chat room. **Requires Python 3 and above**

The host is assumed to be the local computer, but it is trivial and likely necessary to change it. Simply provide a `host` kwarg for `init_server()` and `init_client()` and you'll be good to go. The default port is `31415`, but that can also be changed.

Features:
  1. Lightweight and flexible
  2. Not many dependencies

Many improvements can be made, such as:
  1. No-loss message sending and receiving
  2. Implementing Blocking Remote Events
  3. Concurrent Server

Currently it is impossible to see who is in the server, however when a new client joins a message will appear announcing their arrival. This is subject to change.

This is still an extremely young project. If you wish you can always contribute! ^-^
Of course you can always just... take the files and leave but WHY WOULD YOU?

Please attribute this to Henry Zhang

Version 1.2.git3
