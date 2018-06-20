import os
from keyrings.cryptfile.cryptfile import CryptFileKeyring
kr = CryptFileKeyring()
kr.file_path = os.path.join(os.getcwd(), 'keyring')


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    try:
        MAIL_USERNAME = kr.get_password("scheduled_mail", "MAIL_USER")
        MAIL_PASSWORD = kr.get_password("scheduled_mail", "MAIL_PASSWORD")
        RECIPIENT = kr.get_password("scheduled_mail", "RECIPIENT")
    except ValueError as e:
        print(e)
        quit(1)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True



