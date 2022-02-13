import os

basedir= os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'..','olx.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True


API_KEY = "1862999216:AAHY1Tvkx0muNVuksrvWYEokOn4xqxZw8wQ"