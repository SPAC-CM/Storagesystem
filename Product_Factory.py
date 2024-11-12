import logging
from abc import ABC, abstractmethod
from Products import *


class Product_Factory(ABC):    
    @abstractmethod
    def Get_ID(self):
        # Find en måde at lave unik id
        return range(1, 100)

    @abstractmethod
    def Create_Product(self, product_name : str):
        return I_Product(self.Get_ID, product_name)
    
class Cloth_Factory(Product_Factory):
    def Get_ID(self):
        return range(1, 100)

    def Create_Product(self, product_name, season):
        return Clothing(self.Get_ID(), product_name, season)