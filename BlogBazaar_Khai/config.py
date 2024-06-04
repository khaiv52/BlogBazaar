import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = "minhkhai8252@gmail.com" # Your email that has permission to access Gmail services to send emails
    MAIL_PASSWORD = "pedo pzsk owup ocqa" # Your app-specific email password obtained from 2-step verification in the account management section
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]' # Subject of the email
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER') # Mail sender
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') # Mail receiver
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = os.environ.get("FLASKY_POSTS_PER_PAGE")
    FLASKY_FOLLOWERS_PER_PAGE = os.environ.get("FLASKY_FOLLOWERS_PER_PAGE")
    FLASKY_COMMENTS_PER_PAGE = os.environ.get('FLASKY_COMMENTS_PER_PAGE')
    
    @staticmethod
    def init_app(app):
        pass
        

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:123456@localhost/db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:123456@localhost/db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:123456@localhost/db'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

