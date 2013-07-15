# -*- coding: utf-8 -*-

from __future__ import print_function
import asyncore
import socket
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import TerminalFormatter


class XfDebugServer(asyncore.dispatcher):

    def __init__(self, host='localhost', port=2409):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            handler = XfDebugHandler(sock)

    def handle_connect(self):
        print("Whoa!")
        # print("Listening on {}".format(self.addr))

    def handle_close(self):
        print("\nClosing server...")
        self.close()

    def handle_write(self):
        print("Writting in Server")


class XfDebugHandler(asyncore.dispatcher_with_send):

    def handle_write(self):
        print("Writting in Handler")

    def handle_read(self):
        data = self.recv(8192)
        # TODO: Add support for reading information about from which file and line data were send.
        if data:
            lexer = PhpLexer(startinline=True, encoding='utf-8', stripall=True)
            formatter = TerminalFormatter(encoding='utf-8')
            print(highlight(data, lexer, formatter))
