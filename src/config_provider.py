import configparser as cp


class ConfigProvider:
    def __init__(self):
        self.config = cp.ConfigParser()
        self.config.read("../resources/config.ini")

    def get(self, section, key):
        return self.config[section][key]


config = ConfigProvider()
