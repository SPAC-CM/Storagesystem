from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
Base = declarative_base()

class Catagories(Base):
    __tablename__ = 'catagories'

    CatagoryID = Column(Integer,primary_key=True)
    CatagoryName = Column(String)

class Product(Base):
    __tablename__ = 'product'

class SQL_Manager(object): 
        
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        engine_uri = f"mysql+pymysql://{os.getenv('mysqluser')}:{os.getenv('mysqlpass')}@{os.getenv('mysqlhost')}/ProductBoi"
        Session = sessionmaker(bind = create_engine(engine_uri))
        self.session = Session()

    def create(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

if __name__ == "__main__":
    manager = SQL_Manager()
    catagory = Catagories(CatagoryName="Food")
    manager.create(catagory)
