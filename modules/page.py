class WebTemplate(object):
    def __init__(self, title, content):
        self.__title = title
        self.__content = content

    def render(self):
        eol = "\n"
        html = '<!DOCTYPE html>' + eol + \
               '<html>' + eol + \
               '<head lang="en">' + eol + \
               '<meta charset="UTF-8">' + eol + \
               '<title>MCCP: ' + self.__title + '</title>' + eol + \
               '<link href="http://fonts.googleapis.com/css?family=Source+Code+Pro" rel="stylesheet" type="text/css">' + eol + \
               '<link rel="stylesheet" type="text/css" href="/css/core.css"/>' + eol + \
               '<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>' + eol + \
               '<script src="/js/core.js"></script>' + eol + \
               '<script src="/js/buttons.js"></script>' + eol + \
               '</head>' + eol + \
               '<body>' + eol + \
               '<div id="outer">' + eol + \
               '<div id="navbar">' + eol + \
               '<div id="navbar">' + eol + \
               '<div>MCCP v1.0' + eol + \
               '<ul>' + eol + \
               '<li class="navbar-button" onclick="handleButton(\'logout\')">Logout</li>' + eol + \
               '</ul>' + eol + \
               '</div>' + eol + \
               '</div>' + eol + \
               '</div>' + eol + \
               '<div id="panel">' + eol + \
               '<div id="sections">' + eol + \
               '<ul>' + eol + \
               '<li class="section-button" onclick="location.href=\'/console\'">Console</li>' + eol + \
               '<li class="section-button" onclick="location.href=\'/info\'">Info</li>' + eol + \
               '<li class="section-button">Logs</li>' + eol + \
               '<li class="section-button">Files</li>' + eol + \
               '</ul>' + eol + \
               '</div>' + eol + \
               '<div id="control">' + eol + \
               '<ul>' + eol + \
               '<li class="control-button" onclick="handleButton(\'start\')">Start</li>' + eol + \
               '<li class="control-button" onclick="handleButton(\'stop\')">Stop</li>' + eol + \
               '</ul>' + eol + \
               '<div id="controlStatus" title="stopped"></div>' + eol + \
               self.__content + \
               '</div>' + eol + \
               '</div>' + eol + \
               '</div>' + eol + \
               '</body>' + eol + \
               '</html>'

        return html