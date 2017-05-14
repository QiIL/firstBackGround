from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class Config():
    pass

class ProdConfig():
    pass

class DevConfig():
    engine = create_engine("sqlite:///database.db", echo=True)
    Session = sessionmaker(bind=engine)
    