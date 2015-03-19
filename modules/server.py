import logging
import logging.config
import time

import sys
import os

__author__ = 'drazisil'


from twisted.internet import protocol, reactor


class MineCraftServerProcess(protocol.ProcessProtocol):
    def __init__(self, io, config):
        self.__version = '1.0'

        # hooks to other systems
        # io handler for console support
        self.__io = io
        # config settings from mccp.cfg
        self.config = config
        # process id for process control
        self.__proc_id = None
        # instance of the web server for output
        self.__web_server = None

        # minecraft server port
        self.mc_port = 25567  # needs to be moved to the config section

        # min memory for java
        self.__minMemory = 2048
        # max memory for java
        self.__maxMemory = 3072
        # home directory for minecraft server
        self.__home = config.getConfig('Servers', 'home_path')
        # log path for mccp
        self.__log_path = self.__home + '/logs/mccp.log'
        logging.basicConfig(filename=self.__log_path,
                            level=logging.DEBUG,
                            format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
        self.__logger = logging.getLogger('Mccp')
        # TODO: Not sure why this is needed
        self.__exec = 'java'
        # server jar path and name
        self.__server_jar = config.getConfig('Servers', 'server_jar')
        self.__args = (r"java", "-Xmx%dm" % self.__maxMemory, "-Xms%dm" % self.__minMemory,
                       "-XX:PermSize=256m", "-jar", self.__home + self.__server_jar, "nogui")

        # set server state to stopped
        self.__status = 'stopped'

        # create initial web update
        # time of last update to web
        self.web_last_update = time.time()
        # contents of web update
        self.web_update = ['MCCP ' + self.__version]

        # log that mccp is starting
        self.__logger.info('Starting MCCP ' + self.__version)

    def connectionMade(self):
        self.__status = 'starting'

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
            print 'Server starting...'
            self.update_web('Server starting...')
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

    def handle_cmd(self, line, source):
        delimiter = os.linesep
        # check if internal command
        if line.find('/') == 0:
            self.handle_cmd_internal(line, source)
        elif self.__status == 'running':
            if line.lower().find('stop') == 0:
                print '\'stop\' is not supported. Please use /stop to stop the server.'
                self.update_web('\'stop\' is not supported. Please use /stop to stop the server.')
            # not an internal command, pass though to process
            else:
                self.transport.write(line + delimiter)
        else:
            print 'Server not yet running, please try again later.'
            self.update_web('Server not yet running, please try again later.')

    def start(self):
        # start the minecraft process
        self.__proc_id = reactor.spawnProcess(self, self.__exec, self.__args, path=self.__home)

    def handle_cmd_internal(self, cmd, source):
        delimiter = os.linesep
        if cmd == '/status':
            print 'Current status: ' + self.get_status()
            self.update_web('Current status: ' + self.get_status())
        elif self.__status == 'running':
            if cmd == '/quit':
                if not source == 'console':
                    print 'MCCP can only be exited from command line. Did you mean /stop?'
                    self.update_web('MCCP can only be exited from command line. Did you mean /stop?')
                else:
                    self.__status = 'quitting'
                    print 'Stopping server and exiting program...'
                    self.update_web('Stopping server and exiting program...')
                    self.transport.write('stop' + delimiter)
            elif cmd == '/restart':
                self.__status = 'restarting'
                print 'Restarting server...'
                self.update_web('Restarting server...')
                self.transport.write('stop' + delimiter)
            elif cmd == '/start':
                print 'Server is already running'
                self.update_web('Server is already running')
            elif cmd == '/stop':
                self.__status = 'stopping'
                print 'Stopping server...'
                self.update_web('Stopping server...')
                self.transport.write('stop' + delimiter)
            else:
                print 'Unknown internal command: ' + cmd
                self.update_web('Unknown internal command: ' + cmd)
        elif cmd == '/quit':
            if not source == 'console':
                print 'MCCP can only be exited from command line. Did you mean /stop?'
                self.update_web('MCCP can only be exited from command line. Did you mean /stop?')
            else:
                self.__status = 'quitting'
                print 'Quitting program...'
                self.update_web('Quitting program...')
                if reactor.running:
                    reactor.stop()
                else:
                    sys.exit(-1)
        elif cmd == '/start':
            if not self.__status == 'starting' and not self.__status == 'restarting':
                self.__status = 'starting'
                print 'Starting minecraft...'
                self.update_web('Starting minecraft...')
                self.start()
            else:
                print 'Server is in the process of starting, please wait...'
                self.update_web('Server is in the process of starting, please wait...')
        elif cmd == '/stop':
            print "Minecraft isn't running yet. Maybe try /start ?"
            self.update_web("Minecraft isn't running yet. Maybe try /start ?")
        else:
            print 'Unknown internal command: ' + cmd
            self.update_web('Unknown internal command: ' + cmd)

    def attach(self, server):
        self.__web_server = server

    def update_web(self, data):
        self.web_last_update = time.time()
        self.web_update.append(data)
        self.__logger.info(data)
