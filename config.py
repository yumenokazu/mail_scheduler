import os, sys

from keyrings.cryptfile.cryptfile import CryptFileKeyring
from exceptions import KeyringError


class Config(object):

    def __init__(self):

        self.DEBUG = False
        self.DEVELOPMENT = False
        self.TESTING = False

        # Mail server config
        self.MAIL_SERVER = 'smtp.gmail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_TLS = False
        self.MAIL_USE_SSL = True

        # Mail credentials and recipient
        try:
            kr = CryptFileKeyring()
            kr.file_path = os.path.join(os.getcwd(), 'keyring')
            self.MAIL_USERNAME = kr.get_password("scheduled_mail", "MAIL_USER")
            self.MAIL_PASSWORD = kr.get_password("scheduled_mail", "MAIL_PASSWORD")
            self.RECIPIENT = kr.get_password("scheduled_mail", "RECIPIENT")
        except ValueError as e:
            raise KeyringError("Error while accessing the keyring.") from e

        # Scheduler settings
        self.SCHEDULER_INTERVAL = 1

        # Config file for instances
        self.INSTANCE_PATH = "instances"


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = False


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEVELOPMENT = True
        self.DEBUG = True


class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.TESTING = True



