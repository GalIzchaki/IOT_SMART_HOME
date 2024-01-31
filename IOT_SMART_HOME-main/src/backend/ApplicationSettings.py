import os.path
from configparser import ConfigParser


class AppSettings:

    """
    Singelotone class
    """

    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.broker_password = None
        self.broker_username = None
        self.broker_port = 0
        self.broker_url = None
        self.broker_root_topic = None
        self.simulator_sampel_interval = None
        self.path = './Appsettings.ini'
        self.is_path_exists()

    def is_path_exists(self):
        self.read_app_settings() if (os.path.isfile(self.path)) else self.write_app_settings()

    def write_app_settings(self):
        config = ConfigParser()

        config["broker"] = {
            'url': 'broker.hivemq.com',
            'port': 1883,
            'username': 'GalAriel',
            'password': 'Z1234567!n',
            'root_topic': "318419298_327213906_smart_heater"
        }
        
        config["simulator"] = {
            'sampeling_interval': 10
        }

        with open(self.path, 'w') as config_file:
            config.write(config_file)

        self.read_app_settings()

    def read_app_settings(self):
        parser = ConfigParser()
        parser.read(self.path)

        self.broker_url = parser.get('broker', 'url')
        self.broker_port = int(parser.get('broker', 'port'))
        self.broker_username = parser.get('broker', 'username')
        self.broker_password = parser.get('broker', 'password')
        self.broker_root_topic = parser.get('broker', 'root_topic')
        self.simulator_sampel_interval = parser.get('simulator', 'sampeling_interval')


