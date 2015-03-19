from twisted.protocols import basic

__author__ = 'drazisil'


class MccpConsoleIO(basic.LineReceiver):
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