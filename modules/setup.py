from ConfigParser import SafeConfigParser

__author__ = 'drazisil'


class MccpSetup(object):
    def __init__(self, config_file):
        self.__config_file = config_file
        self.__config = SafeConfigParser()
        self.__config.read(self.__config_file)

    def set_config_defaults(self):
        self.__config.add_section('Servers')
        self.__config.set('Servers', 'home_path', r"/media/Matrix/mc-server-forge-1.8.3")
        self.__config.set('Servers', 'server_jar', r"/forge-1.8-11.14.1.1322-universal.jar")
        self.__config.set('Servers', 'server_port', '25567')
        self.__config.add_section('Web')
        self.__config.set('Web', 'web_port', '8888')
        self.__config.set('Web', 'web_username', 'demo')
        self.__config.set('Web', 'web_password', '89e495e7941cf9e40e6980d14a16bf023ccd4c91')

        # Writing our configuration file to 'mccp.cfg'
        with open(self.__config_file, 'wb') as configfile:
            self.__config.write(configfile)

    # TODO: Check for missing values
    def create_if_not_exists(self):
        # if the config file is not set correctly, create it.
        if not self.__config.has_section('Servers') or not self.__config.has_section('Web'):
            self.set_config_defaults()

    def getConfig(self, section, value):
        return self.__config.get(section, value)