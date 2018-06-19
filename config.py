import os


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECIPIENT = os.environ.get('RECIPIENT')
    SUBJECT = "Schedule"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True




class TestingConfig(Config):
    TESTING = True



