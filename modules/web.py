import os

from twisted.python.components import registerAdapter
from twisted.internet import reactor
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.server import Session
from zope.interface import Interface, Attribute, implements

from modules.page import WebPage


__author__ = 'drazisil'


class ExpireSession(Resource):
    def render_GET(self, request):
        request.getSession().expire()


class IUsername(Interface):
    value = Attribute("A string that holds the username.")


class UserName(object):
    implements(IUsername)

    def __init__(self, session):
        self.value = ''

    def set_name(self, name):
        self.value = name


class RcRoot(Resource):
    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    # this code lets you call the resource as itself, as well as a parent
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        session = request.getSession()
        username = IUsername(session)
        if username.value == '':
            username.value = 'wombat+' + str(os.urandom(8))

        content = '<html>' \
                  '<head>' \
                  '<title>MCCP: Home</title>' \
                  '</head>' \
                  '<body>' \
                  'moo ' + username.value + \
                  '</body>' \
                  '</html>'
        return content


class RcStatus(Resource):
    # isLeaf = True

    def __init__(self, mc_server):
        Resource.__init__(self)
        self.__server = mc_server

    def render_GET(self, request):
        page = WebPage('Status', '', 'Server status: ' + self.__server.get_status())

        return page.render()


class MccpWeb():
    def __init__(self, mc_process, config):
        self.__mc_process = mc_process
        self.__web_port = int(config.get('Web', 'web_port'))
        factory = RcRoot(mc_process)
        factory.putChild('status', RcStatus(mc_process))
        factory.putChild("expire", ExpireSession())
        self.__site = server.Site(factory)
        registerAdapter(UserName, Session, IUsername)


    def start(self):
        reactor.listenTCP(self.__web_port, self.__site)
