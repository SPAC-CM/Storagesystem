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

    def get_item(self,table_name : str, clause : str, item_value : str):
        try:
            if not table_name and not item_value and not clause:
                raise Exception("Delete must have a table name, a clause and a value")
            match clause.lower():
                case "id":
                    if table_name.lower() == "product":
                        return self.session.query(Product).filter(Product.id == int(item_value))
                    elif table_name.lower() == "categories":
                        return self.session.query(Categories).filter(Categories.c.name == int(item_value)).delete()
                case "name":
                    if table_name.lower() == "product":
                        return self.session.query(Product).filter(Product.name == item_value).delete()
                    elif table_name.lower() == "categories":
                        return self.session.query(Categories).filter(Categories.c.name == item_value).delete()
                case "stock":
                    return self.session.query(Product).filter(Product.StockQuantity == int(item_value)).delete()
                case "price":
                    return self.session.query(Product).filter(Product.price == item_value).delete()
                case _:
                    raise Exception("clause not recognized")
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

    def remove_item(self, table_name : str, clause : str, item_value : str):
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        entry = self.get_item(table_name, clause, item_value)
        entry.delete()
        self.session.commit()

if __name__ == '__main__':
    manager = SQL_Manager()
    factory = Factory()
    manager.remove_item(table_name = "Product", clause = "id", item_value = "1")
    table = manager.get_table("Products")
    for row in table:
        print(row)
