import os

variables = {
    'SECRET_KEY' :"M7WBKO4zrnwooYOi03pAexMYicXBN5eo",
    'FILE':  os.path.dirname(os.path.abspath(__file__)).replace("\\", '/')
}

class Config():
    SECRET_KEY = variables['SECRET_KEY']

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI =  f'sqlite:///{variables["FILE"]}' + "/databases/auth.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SERVER_NAME = "localhost:5000"

config = {
    'development': DevelopmentConfig,
}