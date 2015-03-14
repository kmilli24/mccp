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
        html = '<div id ="wrap" style="width:750px; margin:0 auto;">' + eol + \
               '<div id ="nav" style="margin: auto; width: 768px; border: 1px solid black;">' + eol + \
               '</div>' + eol + \
               '<div id ="sidebar" style="margin: auto; width: 768px; border: 1px solid black;">' + eol + \
               '</div>' + eol + \
               '<div id ="main" style="float:right; width:500px;">' + eol + \
               self.__content + eol + \
               '</div>' + eol + \
               '<div id ="footer" style="clear: both;">' + eol + \
               '</div>' + eol + \
               '</div>'
        return html


class WebCSS(object):
    def __init__(self, content):
        pass