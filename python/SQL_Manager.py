from sqlalchemy import create_engine, MetaData, select, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
from classes.Tables import *
from classes.Factory import *
class SQL_Manager(object):

    _instance = None
    def __new__(cls):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.engine_uri = f"mysql+pymysql://{os.getenv('mysqluser')}:{os.getenv('mysqlpass')}@{os.getenv('mysqlhost')}/Products"
        engine = create_engine(self.engine_uri)
        self.metadata = create_tables(MetaData())
        self.metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        self.engine = engine

    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

    def get_item(self,table_name : str, parametor : str, item_value : str):
        try:
            if not table_name and not item_value and not parametor:
                raise Exception("Delete must have a table name, a parametor and a value")
            match parametor.lower():
                case "id":
                    if table_name.lower() == "product":
                        return self.session.query(Product).filter(Product.id == int(item_value))
                    elif table_name.lower() == "categories":
                        return self.session.query(Categories).filter(Categories.c.name == int(item_value))
                case "name":
                    if table_name.lower() == "product":
                        return self.session.query(Product).filter(Product.name == item_value)
                    elif table_name.lower() == "categories":
                        return self.session.query(Categories).filter(Categories.c.name == item_value)
                case "stock":
                    return self.session.query(Product).filter(Product.StockQuantity == int(item_value))
                case "price":
                    return self.session.query(Product).filter(Product.price == item_value)
                case _:
                    raise Exception("parametor not recognized")
            self.session.commit()
        except Exception as e:
            print(e)

    def get_table(self, table_name: str):
        self.session.close()
        engine = create_engine(self.engine_uri)
        self.metadata = create_tables(MetaData())
        self.metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        match table_name.lower():
            case "products":
                cmd = select(Product)
            case "category":
                cmd = select(Categories)
        table = self.session.execute(cmd)
        return table

    def remove_item(self, table_name : str, parametor : str, item_value : str):
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        entry = self.get_item(table_name, parametor, item_value)
        entry.delete()
        self.session.commit()

if __name__ == '__main__':
    manager = SQL_Manager()
    factory = Factory()
    manager.remove_item(table_name = "Product", parametor = "id", item_value = "1")
    table = manager.get_table("Products")
    for row in table:
        print(row)
