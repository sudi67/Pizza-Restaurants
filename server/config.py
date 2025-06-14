import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, '..', 'db.json')) as f:
    db_config = json.load(f)

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
