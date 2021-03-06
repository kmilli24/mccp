import cgi
import sys

from twisted.internet.error import CannotListenError

from twisted.python.components import registerAdapter
from twisted.internet import reactor
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.server import Session
from twisted.web.static import File
from twisted.web.util import Redirect
from zope.interface import Interface, Attribute, implements
import simplejson as json

from modules.page import WebTemplate


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


class RcLogin(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    @staticmethod
    def render_GET(request):
        session_id = request.getSession()
        session = ISession(session_id)
        user = session.username
        if user == '':
            return File('./pages/login.html').render(request)
        else:
            return Redirect("/console").render(request)


class RcInfo(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    def render_GET(self, request):
        session_id = request.getSession()
        session = ISession(session_id)
        user = session.username
        if user == '':
            return File('./pages/login.html').render(request)
        else:
            html = '<div id="info">' + self.__server.mc_version + '</div>'
            page = WebTemplate('Info', html).render()
            return page


class RcConsole(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    @staticmethod
    def render_GET(request):
        session_id = request.getSession()
        session = ISession(session_id)
        user = session.username
        if not user == '':
            return File('./pages/index.html').render(request)
        else:
            return Redirect("/login").render(request)


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
        return Redirect("/console").render(request)


class RcCmd(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    # noinspection PyUnusedLocal
    @staticmethod
    def render_GET(request):
        # just so there's no error on a get
        return '<html></html>'

    def render_POST(self, request):
        session = ISession(request.getSession())
        if 'action' in request.args:
            # This is an action
            action = cgi.escape(request.args["action"][0])
            if action == 'login':
                username = cgi.escape(request.args["username"][0])
                password = cgi.escape(request.args["password"][0])
                if username == self.__server.config.get_config('Web', 'web_username'):
                    if password == self.__server.config.get_config('Web', 'web_password'):
                        session.username = username
                        return Redirect('/console').render(request)
        elif 'button' in request.args:
            # This is a button
            button = cgi.escape(request.args["button"][0])
            if button == 'logout':
                session.username = ''
                return Redirect('/console').render(request)
            elif not session.username == '':
                if button == 'start':
                    # only send the command to the server if logged in
                    self.__server.handle_cmd(cgi.escape('/start'), cgi.escape(request.args["source"][0]))
                elif button == 'stop':
                    # only send the command to the server if logged in
                    self.__server.handle_cmd(cgi.escape('/stop'), cgi.escape(request.args["source"][0]))
            elif 'cmd' in request.args:
                # only send the command to the server if logged in
                self.__server.handle_cmd(cgi.escape(request.args["cmd"][0]), cgi.escape(request.args["source"][0]))
        return '<html></html>'


class MccpWeb():
    def __init__(self, mc_process, config):
        self.__mc_process = mc_process
        self.__web_port = int(config.get_config('Web', 'web_port'))
        factory = RcRoot(mc_process)
        factory.putChild('login', RcLogin(mc_process))
        factory.putChild('console', RcConsole(mc_process))
        factory.putChild('info', RcInfo(mc_process))
        factory.putChild('css', File('./pages/css'))
        factory.putChild('js', File('./pages/js'))
        factory.putChild('img', File('./pages/img'))
        factory.putChild('term', RcTerm(mc_process))
        factory.putChild('cmd', RcCmd(mc_process))
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
