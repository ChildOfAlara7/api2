import os
import configparser
basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read("config.ini")
db_path = 'postgresql' + "://" + config["PSQL"]['user'] + ":" + config["PSQL"]['password'] + "@" + config["PSQL"]['host'] + ":" + config["PSQL"]['port'] + '/' + config["PSQL"]['database']


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False