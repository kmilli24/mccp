__author__ = 'drazisil'


class WebPage(object):
    def __init__(self, title, head, body):
        self.__title = title
        self.__head = head
        self.__body = body

    def render(self):
        html = '<html>' \
               '<head>' \
               '<title>MCCP: ' + self.__title + '</title>' \
                                                '<meta http-equiv="refresh" content="3">' + \
               self.__head + \
               '</head>' \
               '<body>' + \
               self.__body + \
               '</body>' \
               '</html>'
        return html