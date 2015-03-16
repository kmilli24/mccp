#!/usr/bin/env python
import ConfigParser
# import argparse

from twisted.internet import stdio
from twisted.protocols import basic

from modules.web import *
from modules.server import MineCraftServerProcess


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


def set_config_defaults(config):
    config.add_section('Servers')
    config.set('Servers', 'home_path', r"/media/Matrix/mc-server-forge-1.8.3")
    config.set('Servers', 'server_jar', r"/forge-1.8-11.14.1.1322-universal.jar")
    config.add_section('Web')
    config.set('Web', 'web_port', '8888')

    # Writing our configuration file to 'mccp.cfg'
    with open('mccp.cfg', 'wb') as configfile:
        config.write(configfile)


def main():
    # parser = argparse.ArgumentParser(description='MCCP is a Minecraft server control wrapper.')
    # parser.add_argument('--name', required=True, help='I\'m a wombat')
    # args = parser.parse_args()

    config = ConfigParser.SafeConfigParser()
    config.read('mccp.cfg')

    # if the config file is not set correctly, create it.
    if not config.has_section('Servers') or not config.has_section('Web'):
        set_config_defaults(config)

    stdio_handler = IOHandler()
    mc_process = MineCraftServerProcess(stdio_handler, config)
    # attach minecraft process to the io handler
    stdio_handler.attach(mc_process)
    # set io handler as default io
    stdio.StandardIO(stdio_handler)

    # start the minecraft process
    # mc_process.start()

    # start the web interface
    site = MccpWeb(mc_process, config)
    site.start()

    # start the twisted reactor loop
    reactor.run()


if __name__ == '__main__':
    main()
