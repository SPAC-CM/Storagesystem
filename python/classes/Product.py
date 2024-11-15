from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import os

base = declarative_base()

# Definer produkter under kategorien "Elektronik"
class Product(base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    price = Column(Float, nullable=False)
    StockQuantity = Column(Integer, nullable=False)
    # CatagoryID = Column(Integer, ForeignKey('Catagories.CatagoryID'))

    # # Relationship til kategori
    # catagory = relationship("Catagory", back_populates="products")

    def __repr__(self):
        return (f"<Product(ProductID={self.id}, ProductName='{self.name}', "
                f"Price={self.price}, StockQuantity={self.StockQuantity}, ")
                # f"Catagory='{self.catagory.CatagoryName if self.catagory else None}')>")
