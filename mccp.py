#!/usr/bin/env python
from twisted.internet import stdio
from twisted.protocols import basic

from modules.setup import MccpSetup
from modules.web import *
from modules.server import MineCraftServerProcess


__author__ = 'drazisil'


class IOHandler(basic.LineReceiver):
    def __init__(self):
        self.__process = ''

    import os

    delimiter = os.linesep

    def connectionMade(self):
        pass

    def rawDataReceived(self, data):
        pass

    def lineReceived(self, line):
        # send the line to minecraft
        self.__process.handle_cmd(line, 'console')

    def attach(self, process):
        self.__process = process


def main():
    # setup the config file
    config = MccpSetup('mccp.cfg')
    config.create_if_not_exists()

    stdio_handler = IOHandler()
    mc_process = MineCraftServerProcess(stdio_handler, config)
    # attach minecraft process to the io handler
    stdio_handler.attach(mc_process)
    # set io handler as default io
    stdio.StandardIO(stdio_handler)

    # start the web interface
    site = MccpWeb(mc_process, config)
    site.start()

    # start the twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    main()
