from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Config(object):
    CSRF_ENABLE = True
    SECRET_KEY = '52afe750351a806309b8976ac293c518'
    

class ProdConfig():
    pass

class DevConfig(Config):
    engine = create_engine("sqlite:////home/qill/workplace/firstPro/app/database.db", echo=True)
    Session = sessionmaker(bind=engine)
    