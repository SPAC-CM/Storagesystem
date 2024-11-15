from Product import *
from Category import *
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Factory(object):
    
    def create_class(self, class_name : str, **kwargs) -> DeclarativeMeta :
        try:
            match(class_name):
                
                case "Product":
                    product = Product()
                    if not "name" in kwargs:
                        raise Exception("Product must name a name")
                    if not "price" in kwargs:
                        raise Exception("Product must have a price")
                    if not "stock" in kwargs:
                        raise Exception("Product must have a stock")
                    product.name = kwargs["name"]
                    product.price = kwargs["price"]
                    product.StockQuantity = kwargs["stock"]
                    return product
                
                case "Category":
                        category = Category()
                        if not "name" in kwargs:
                            raise Exception("Catagory must have a name")
                        category.CategoryName = kwargs["name"]
                        return category
                    
                case _:
                    raise Exception("Table name not recognized")
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    factory = Factory()
    test = factory.create_class("Product", name = "Nikeke", price = 100, stock = 0)
    test2 = factory.create_class("Category", name = "Off brand")
    print(test)
    print(test2)
    