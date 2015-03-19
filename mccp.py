from twisted.internet import stdio, reactor

from modules.io import MccpConsoleIO
from modules.setup import MccpSetup
from modules.server import MineCraftServerProcess
from modules.web import MccpWeb


def main():
    # setup the config file
    config = MccpSetup('mccp.cfg')
    config.check_missing_keys()

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
