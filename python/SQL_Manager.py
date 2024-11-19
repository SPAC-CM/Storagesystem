from sqlalchemy import create_engine, MetaData, select, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
from classes.Tables import *
from classes.Factory import *
class SQL_Manager(object):

    _instance = None
    def __new__(cls, user : str, password : str, host: str):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, user : str, password : str, host: str):
        self.engine_uri = f"mysql+pymysql://"+user+":"+password+"@"+host+"/Products"
        engine = create_engine(self.engine_uri)
        self.metadata = create_tables(MetaData())
        self.metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        self.engine = engine

    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

    def multi_query(self, **kwargs):
        queries = []
        for key in kwargs.keys():
            table, parametor ,item_value = kwargs[key]
            queries.append(self.get_query(table, parametor, item_value))
        item = queries[0]
        for i in range(1,len(queries)):
            item = item.intersect(queries[i])
        return item.all()

    def get_query(self,table_name : str, parametor : str, item_value : str):
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
                    if not table_name.lower() == "product":
                        raise Exception("only products can have stock")
                    return self.session.query(Product).filter(Product.StockQuantity == int(item_value))
                case "price":
                    if not table_name.lower() == "product":
                        raise Exception("only products can have price")
                    return self.session.query(Product).filter(Product.price == item_value)
                case _:
                    raise Exception("parametor not recognized")
            self.session.commit()
        except Exception as e:
            print(e)
    
    def get_item(self,table_name : str, parametor : str, item_value : str):
        item = self.get_query(table_name,parametor,item_value)
        return item.all()

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

    def update_item(self, table_name : str, parametor : str, item_value : str, update_parametor : str, update_value : str):
        item = self.get_query(table_name, parametor, item_value)
        try:
            match update_parametor.lower():
                case "name":
                    if table_name.lower() == "product":
                        item.update({Product.name: update_value})
                    elif table_name.lower() == "categories":
                        item.update({Category.CategoryName: update_value})
                    else:
                        raise Exception("table name not recognized")
                case "stock":
                    if not table_name.lower() == "product":
                        raise Exception("Can only update stock for products")
                    item.update({Product.StockQuantity: int(update_value)})
                case "price":
                    if not table_name.lower() == "product":
                        raise Exception("Can only update price for products")
                    item.update({Product.price: float(update_value)})
                case _:
                    raise Exception("parametor not recognized")
            self.session.commit()
        except Exception as e:
            print(e)

    def remove_item(self, table_name : str, parametor : str, item_value : str):
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        entry = self.get_query(table_name, parametor, item_value)
        entry.delete()
        self.session.commit()

if __name__ == '__main__':
    manager = SQL_Manager(os.getenv('mysqluser'),os.getenv('mysqlpass'),os.getenv('mysqlhost'))
    print(str(manager.multi_query(first = ("product","price","10"), second = ("product", "stock", "5"))))
