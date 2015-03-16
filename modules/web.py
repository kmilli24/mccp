import cgi
import os
import sys

from twisted.internet.error import CannotListenError

from twisted.python.components import registerAdapter
from twisted.internet import reactor
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.server import Session
from twisted.web.static import File
from zope.interface import Interface, Attribute, implements
import simplejson as json

from modules.page import WebPage, WebTemplate


__author__ = 'drazisil'


class ExpireSession(Resource):
    @staticmethod
    def render_GET(request):
        request.getSession().expire()


class ISession(Interface):
    username = Attribute("A string that holds the username.")


class MccpSession(object):
    implements(ISession)

    # noinspection PyUnusedLocal
    def __init__(self, session):
        self.username = ''


class RcTerm(Resource):
    def __init__(self, process):
        Resource.__init__(self)
        self.__process = process

    # noinspection PyUnusedLocal
    def render_GET(self, request):
        obj = {'status': self.__process.get_status(), 'timestamp': self.__process.web_last_update,
               'output': self.__process.web_update}

        return json.dumps(obj, separators=(',', ':'), sort_keys=True)


class RcRoot(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    # this code lets you call the resource as itself, as well as a parent
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    @staticmethod
    def render_GET(request):
        session_id = request.getSession()
        session = ISession(session_id)
        if session.username == '':
            session.username = str(os.urandom(16))

        page = WebPage('Home', '', WebTemplate('wombat ' + str(session.username)).render())

        return page.render()


class RcCmd(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    def render_POST(self, request):
        self.__server.handle_cmd(cgi.escape(request.args["cmd"][0]), cgi.escape(request.args["source"][0]))
        return '<html></html>'


class MccpWeb():
    def __init__(self, mc_process, config):
        self.__mc_process = mc_process
        self.__web_port = int(config.getConfig('Web', 'web_port'))
        factory = RcRoot(mc_process)
        factory.putChild('core', File('./pages'))
        factory.putChild('term', RcTerm(mc_process))
        factory.putChild('cmd', RcCmd(mc_process))
        factory.putChild('expire', ExpireSession())
        self.__site = server.Site(factory)
        registerAdapter(MccpSession, Session, ISession)

    def start(self):
        try:
            reactor.listenTCP(self.__web_port, self.__site)
        except CannotListenError:
            print 'Port ' + str(self.__web_port) + ' already in use.'
            if reactor.running:
                reactor.stop()
            else:
                sys.exit(-1)
