from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
from classes.Tables import *
from classes.Factory import *
from classes.Product import *
class SQL_Manager(object):

    _instance = None
    def __new__(cls):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        engine_uri = f"mysql+pymysql://root:bWsEocb2r706!@127.0.0.1/Products"
        engine = create_engine(engine_uri)
        metadata = create_tables(MetaData())
        metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(engine_uri))
        
        self.session = Session()

    def add_table(self, table_name : str):
        print("horse")

    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()


if __name__ == '__main__':
    manager = SQL_Manager()
