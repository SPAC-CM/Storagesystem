from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
class SQL_Manager(object):

    _instance = None
    def __new__(cls):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        engine_uri = f"mysql+pymysql://{os.getenv('mysqluser')}:{os.getenv('mysqlpass')}@{os.getenv('mysqlhost')}/Products"
        Session = sessionmaker(bind = create_engine(engine_uri))
        self.session = Session()

    def add_table(self, table_name : str):
        print("horse")

    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()


if __name__ == '__main__':
    catagory = Category(name="Stuff")
    manager = SQL_Manager()
    manager.add_item(catagory)
