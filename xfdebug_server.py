# -*- coding: utf-8 -*-

from __future__ import print_function
import asyncore
import colorama
import os
import socket
from pygments import highlight
from pygments.lexers import PhpLexer
from pygments.formatters import TerminalFormatter


class XfDebugServer(asyncore.dispatcher):

    def __init__(self, host='127.0.0.1', port=2409):
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


class XfDebugHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)

        if data:
            colorama.init()
            lines = data.split("\n")
            for num, line in enumerate(lines):
                if '[TRACE]' in line:
                    type, msg = line.split()
                    print((msg, os.getcwd()))
                    if msg.startswith(os.getcwd()):
                        msg = msg[len(os.getcwd()):]
                    print(colorama.Back.GREEN + colorama.Fore.WHITE + type, end=' ')
                    print(colorama.Back.RESET + colorama.Fore.MAGENTA + msg)
                    del lines[num]
            data = "\n".join(lines)

            lexer = PhpLexer(startinline=True, encoding='utf-8', stripall=True)
            formatter = TerminalFormatter(encoding='utf-8')
            print(colorama.Style.RESET_ALL + highlight(data, lexer, formatter))
