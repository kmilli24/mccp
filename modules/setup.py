from ConfigParser import SafeConfigParser
import sys


class MccpSetup(object):
    def __init__(self, config_file):
        self.__config_file = config_file
        self.__config = SafeConfigParser()
        self.__config.read(self.__config_file)
        self.__config_keys = {'Servers': ['home_path', 'server_jar', 'server_port'],
                              'Web': ['web_port', 'web_username', 'web_password']}

    def set_config_defaults(self, section):
        if section == 'Servers':
            self.__config.add_section('Servers')
            self.__config.set('Servers', 'home_path', r"/media/Matrix/mc-server-forge-1.8.3")
            self.__config.set('Servers', 'server_jar', r"/forge-1.8-11.14.1.1322-universal.jar")
            self.__config.set('Servers', 'server_port', '25567')
        elif section == 'Web':
            self.__config.add_section('Web')
            self.__config.set('Web', 'web_port', '8888')
            self.__config.set('Web', 'web_username', 'demo')
            self.__config.set('Web', 'web_password', '89e495e7941cf9e40e6980d14a16bf023ccd4c91')

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