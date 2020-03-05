import os
class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://alexkhan:1234testWave@localhost/calltronix'

    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    DEBUG = True
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Flask-User settings
    # USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    # USER_ENABLE_EMAIL = True        # Enable email authentication
    # USER_ENABLE_USERNAME = False    # Disable username authentication
    # USER_EMAIL_SENDER_NAME = USER_APP_NAME
    # USER_EMAIL_SENDER_EMAIL = os.environ.get("USER_EMAIL_SENDER_EMAIL")




class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
  
    pass


config_options = {
    'development':DevConfig,
    'production':ProdConfig
}     