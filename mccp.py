#!/usr/bin/env python
from twisted.internet import stdio

from modules.io import MccpConsoleIO
from modules.setup import MccpSetup
from modules.web import *
from modules.server import MineCraftServerProcess


__author__ = 'drazisil'


def main():
    # setup the config file
    config = MccpSetup('mccp.cfg')
    config.create_if_not_exists()

    stdio_handler = MccpConsoleIO()
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
