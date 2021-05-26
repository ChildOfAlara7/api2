from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
from flask import g
from flask import current_app

config = configparser.ConfigParser()
config.read("config.ini")
db_path = 'postgresql' + "://" + config["PSQL"]['user'] + ":" + config["PSQL"]['password'] + "@" + config["PSQL"]['host'] + ":" + config["PSQL"]['port'] + '/' + config["PSQL"]['database']

def get_db():
    if "db" not in g:
        g.db = create_engine(db_path)

    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.execute(f.read().decode("utf8"))
