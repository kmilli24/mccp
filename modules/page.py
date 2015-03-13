__author__ = 'drazisil'


class WebPage(object):
    def __init__(self, title, head, body):
        self.__title = title
        self.__head = head
        self.__body = body

    def render(self):
        eol = "\n"
        html = '<html>' + eol + \
               '<head>' + eol + \
               '<title>MCCP: ' + self.__title + '</title>' + eol + \
               '<meta http-equiv="refresh" content="3">' + eol + \
               self.__head + eol + \
               '</head>' + eol + \
               '<body>' + eol + \
               self.__body + eol + \
               '</body>' + eol + \
               '</html>'
        return html


class WebTemplate(object):
    def __init__(self, content):
        self.__content = content

    def render(self):
        eol = "\n"
        html = '<div style="margin: auto; width: 600px; border: 1px solid black;">' + eol + \
               self.__content + eol + \
               '</div>'
        return html


class WebCSS(object):
    def __init__(self, content):
        pass