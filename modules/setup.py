from ConfigParser import SafeConfigParser
import hashlib
import sys


class MccpSetup(object):
    def __init__(self, config_file):
        self.__config_file = config_file
        self.__config = SafeConfigParser()
        self.__config.read(self.__config_file)
        self.__config_keys = {'Web': ['web_password', 'web_username', 'web_port'],
                              'Servers': ['server_port', 'server_jar', 'home_path']}

    def set_config_defaults(self, section):
        if section == 'Servers':
            self.__config.add_section('Servers')
            home_path = ''
            while home_path == '':
                home_path = raw_input('Minecraft path : ')
            self.__config.set('Servers', 'home_path', home_path or r"/media/Matrix/mc-server-forge-1.8.3")
            self.__config.set('Servers', 'server_jar', r"/forge-1.8-11.14.1.1322-universal.jar")
            server_port = raw_input('Server port [25565] : ')
            self.__config.set('Servers', 'server_port', server_port or '25565')
        elif section == 'Web':
            self.__config.add_section('Web')
            web_port = raw_input('Web port [80] : ')
            self.__config.set('Web', 'web_port', web_port or '80')
            web_user = ''
            while web_user == '':
                web_user = raw_input('Web username : ')
            self.__config.set('Web', 'web_username', web_user)
            web_pass = ''
            while web_pass == '':
                web_pass = raw_input('Web password : ')
            web_pass = hashlib.sha1(web_pass).hexdigest()
            self.__config.set('Web', 'web_password', web_pass)

        # Writing our configuration file to 'mccp.cfg'
        with open(self.__config_file, 'wb') as configfile:
            self.__config.write(configfile)

    def check_missing_keys(self):
        for section in self.__config_keys:
            if not self.__config.has_section(section):
                self.set_config_defaults(section)
            for key in self.__config_keys[section]:
                if not self.__config.has_option(section, key):
                    print 'Section ' + section + ' is missing key ' + key
                    sys.exit(-1)

    def get_config(self, section, value):
        return self.__config.get(section, value)
