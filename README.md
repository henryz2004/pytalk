# Pytalk
Chat Program developed entirely in Python and Kivy.

PyTalk is a simple and lightweight Kivy-based chat application that uses sockets. I made it Because I Can, and it is built on top of an event based framework `Pynet` (which is also made by me). Find the framework inside the `pytalk` folder. The chat application is easily expandable; you can add custom Remote Events or use the networking framework by itself for a completely different task. The only non-standard-library dependency this relies on is Kivy, which can be easily installed using pip.

To run, first run `chatserver.py` in the background. This will start a server that the client can connect to. Then, in a separate command prompt (or just run concurrently), run `clientgui.py`. After a bunch of omnious error-like startup messages from kivy, a window should come up (if there's a server to connect to). Enter your alias (a user system has not been set up yet) and then press continue. After that you have officially entered the chat room. **Requires Python 3 and above**

The host is assumed to be the local computer, but it is trivial and likely necessary to change it. Simply provide a `host` kwarg for `init_server()` and `init_client()` and you'll be good to go. The default port is `31415`, but that can also be changed.

Features:
  1. Lightweight and flexible
  2. Not many dependencies
  3. Remote Events which allow for greater developer freedom
  4. Socket-based
  5. Threaded client, so adding a GUI is easy
  6. Designed with security in mind

Many improvements can be made, such as:
  1. Removing the `Message` class
  2. No-loss message sending and receiving
  3. Implementing Blocking Remote Events
  4. Concurrent Server

Currently it is impossible to see who is in the server, however when a new client joins a message will appear announcing their arrival. This is subject to change.

This is still an extremely young project. If you wish you can always contribute! ^-^
Of course you can always just... take the files and leave but WHY WOULD YOU?

Version 1.0.git10
Please attribute this to Henry Zhang
