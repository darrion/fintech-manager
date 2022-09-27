import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    APP_SETTINGS = os.environ['APP_SETTINGS']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = True