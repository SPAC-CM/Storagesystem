from sqlalchemy import create_engine, MetaData, select, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
from classes.Tables import *
from classes.Factory import *

#The ORM connection between the database and API
class SQL_Manager(object):

    #Insures that no other instances of the ORM can exist at any given point
    _instance = None
    def __new__(cls, user : str, password : str, host: str):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    #Creates the manager and initializes the connection
    def __init__(self, user : str, password : str, host: str):
        self.engine_uri = f"mysql+pymysql://"+user+":"+password+"@"+host+"/Products"
        engine = create_engine(self.engine_uri)
        self.metadata = create_tables(MetaData())
        self.metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        self.engine = engine

    #Takes an item from the factory and inserts it into the database
    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

    #Takes multiple search parametors to do a search for all of them. The parametors are like in the get query function but must be given as a tuple
    #Example multi_query(first_query=("product", "name", "example"), second_query=("product", "category", "1"), ...)
    def multi_query(self, **kwargs):

        #Collects all the queries
        queries = []

        #Runs thru each of them tuples and calls a single get querry
        for key in kwargs.keys():
            table, parametor ,item_value = kwargs[key]
            queries.append(self.get_query(table, parametor, item_value))

        #Finds uses intersect to find the item fulfilling all queries
        item = queries[0]
        for i in range(1,len(queries)):
            item = item.intersect(queries[i])
        return item.all()

    #Gets a single query.
    def get_query(self,table_name : str, parametor : str, item_value : str):
        try:
            #Switch to find which coloumn to look in and matches items with the item value
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
                    return self.session.query(Product).filter(Product.price == float(item_value))
                case "category":
                    if not table_name.lower() == "product":
                        raise Exception("only products have a category")
                    return self.session.query(Product).filter(Product.category_id==int(item_value))
                case _:
                    raise Exception("parametor not recognized")
        except Exception as e:
            print(e)
    
    #Gets all items where the parametor fulfills the item_value
    def get_item(self,table_name : str, parametor : str, item_value : str):
        item = self.get_query(table_name,parametor,item_value)
        print(item)
        return item.all()

    #Gets a single table
    def get_table(self, table_name: str):
        match table_name.lower():
            case "products":
                cmd = select(Product)
            case "category":
                cmd = select(Categories)
        table = self.session.execute(cmd)
        return table

    #Updates items where the parametor matches the item_value. The update_parametor specifies which coloumn must be changed and the update_value is the new value
    def update_item(self, table_name : str, parametor : str, item_value : str, update_parametor : str, update_value : str):

        #Gets all items that matches the search criteria
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
                case "category":
                    if not table_name.lower() == "product":
                        raise Exception("Can only update category for products")
                    item.update({Product.category_id: int(update_value)})
                case _:
                    raise Exception("parametor not recognized")
            self.session.commit()
        except Exception as e:
            print(e)

    #Deletes items where the parametor matches the item_value
    def remove_item(self, table_name : str, parametor : str, item_value : str):
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        entry = self.get_query(table_name, parametor, item_value)
        entry.delete()
        self.session.commit()

if __name__ == '__main__':
    manager = SQL_Manager(os.getenv('mysqluser'),os.getenv('mysqlpass'),os.getenv('mysqlhost'))
    factory = Factory()
    product = factory.create_class("product", name="Test", price=10,stock = 10, category=2)
    manager.add_item(product)
