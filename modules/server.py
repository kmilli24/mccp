import time

__author__ = 'drazisil'

import sys
import os

from twisted.internet import protocol, reactor


class MineCraftServerProcess(protocol.ProcessProtocol):
    def __init__(self, io, config):
        self.__io = io
        self.__web_server = None
        self.web_last_update = time.time()
        self.web_update = []
        self.__mc_port = 25567  # needs to be moved to the config section
        self.__minMemory = 2048
        self.__maxMemory = 3072
        self.__home = config.get('Servers', 'home_path')
        self.__status = 'stopped'
        self.__exec = 'java'
        self.__server_jar = config.get('Servers', 'server_jar')
        self.__args = (r"java", "-Xmx%dm" % self.__maxMemory, "-Xms%dm" % self.__minMemory,
                       "-XX:PermSize=256m", "-jar", self.__home + self.__server_jar, "nogui")

    def connectionMade(self):
        self.__status = 'starting'
        print 'Server starting...'

    def outReceived(self, data):
        # server loaded
        if data.find('Done (') != -1:
            print 'Server Ready!'
            self.update_web('Server Ready!')
            self.__status = 'running'
        # port in use
        elif data.find('**** FAILED TO BIND TO PORT!') != -1:
            print 'Server failed to start!'
            print 'MC: ' + data,
            self.update_web(data)
            self.transport.signalProcess('KILL')
            if reactor.running:
                reactor.stop()
            else:
                sys.exit(-1)

        if self.__status == 'running':
            print 'MC: ' + data,
            self.update_web(data)
            # else:
            # print 'MC: ' + data,

    def errReceived(self, data):
        # error pipe for java
        # print 'MC-ERR: ' + data,
        pass

    def processEnded(self, reason):
        print 'Server stopped!'
        self.update_web('Server stopped!')
        if self.__status == 'restarting':
            self.start()
        elif self.__status == 'stopping':
            # minecraft has quit
            self.__status = 'stopped'
            pass
        else:
            self.__status = 'quitting'
            # program quit requested, stop the reactor and exit
            reactor.stop()

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def handle_cmd(self, line):
        delimiter = os.linesep
        # check if internal command
        if line.find('/') == 0:
            self.handle_cmd_internal(line)
        elif self.__status == 'running':
            if line.lower().find('stop') == 0:
                print '\'stop\' is not supported. Please use /stop to stop the server.'
                self.update_web('\'stop\' is not supported. Please use /stop to stop the server.')
            # not an internal command, pass though to process
            else:
                self.transport.write(line + delimiter)
        else:
            print 'Server not yet running, please try again later.',

    def start(self):
        # start the minecraft process
        reactor.spawnProcess(self, self.__exec, self.__args, path=self.__home)

    def handle_cmd_internal(self, cmd):
        delimiter = os.linesep
        if cmd == '/status':
            print 'Current status: ' + self.get_status()
            self.update_web('Current status: ' + self.get_status())
        elif self.__status == 'running':
            if cmd == '/quit':
                self.__status = 'quitting'
                print 'Stopping server and exiting program...'
                self.update_web('Stopping server and exiting program...')
                self.transport.write('stop' + delimiter)
            elif cmd == '/restart':
                self.__status = 'restarting'
                print 'Restarting server...'
                self.update_web('Restarting server...')
                self.transport.write('stop' + delimiter)
            elif cmd == '/stop':
                self.__status = 'stopping'
                print 'Stopping server...'
                self.update_web('Stopping server...')
                self.transport.write('stop' + delimiter)
            else:
                print 'Unknown internal command: ' + cmd
                self.update_web('Unknown internal command: ' + cmd)
        elif cmd == '/quit':
            self.__status = 'quitting'
            print 'Quitting program...'
            self.update_web('Quitting program...')
            if reactor.running:
                reactor.stop()
            else:
                sys.exit(-1)
        elif cmd == '/start':
            self.__status = 'starting'
            print 'Starting minecraft...'
            self.update_web('Starting minecraft...')
            self.start()
        else:
            print 'Unknown internal command: ' + cmd
            self.update_web('Unknown internal command: ' + cmd)

    def attach(self, server):
        self.__web_server = server

    def update_web(self, data):
        self.web_last_update = time.time()
        self.web_update.append(data)