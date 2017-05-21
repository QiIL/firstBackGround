from flask import Flask
from config import DevConfig, Config
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object(DevConfig)
Base = declarative_base()
session = DevConfig.Session()

from app import views, models
