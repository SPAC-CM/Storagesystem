from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import os

base = declarative_base()

# Definer kategorien "Elektronik" og "Refurbished Elektronik"
class Catagory(base):
    __tablename__ = 'Catagories'

    CatagoryID = Column(Integer, primary_key=True)
    CatagoryName = Column(String(15), nullable=False)

    # Relationship tilknytter produkter til kategorien
    products = relationship("Product", back_populates="catagory")

    def __repr__(self):
        return f"<Catagory(CatagoryID={self.CatagoryID}, CatagoryName='{self.CatagoryName}')>"

# Definer produkter under kategorien "Elektronik"
class Product(base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float, nullable=False)
    StockQuantity = Column(Integer, default=0)
    CatagoryID = Column(Integer, ForeignKey('Catagories.CatagoryID'))

    # Relationship til kategori
    catagory = relationship("Catagory", back_populates="products")

    def __repr__(self):
        return (f"<Product(ProductID={self.id}, ProductName='{self.name}', "
                f"Price={self.price}, StockQuantity={self.StockQuantity}, "
                f"Catagory='{self.catagory.CatagoryName if self.catagory else None}')>")

# Opretter engine og session
# Kommentar: Venter med at opsætte databaseforbindelsen, da jeg er i tvivl omkring opsætningen

# Opret kategorier: "Elektronik" og "Refurbished Elektronik"
elektronik_category = Catagory(CatagoryName="Elektronik")
refurbished_category = Catagory(CatagoryName="Refurbished Elektronik")

# Opret produkter relateret til elektronik
prod1 = Product(name="Smartphone", price=699.99, StockQuantity=50, catagory=elektronik_category)
prod2 = Product(name="Laptop", price=1299.99, StockQuantity=30, catagory=elektronik_category)
prod3 = Product(name="Smart TV", price=7000, StockQuantity=45, catagory=elektronik_category)
prod4 = Product(name="Headphones", price=199.99, StockQuantity=150, catagory=elektronik_category)
prod5 = Product(name="Smartwatch", price=299.99, StockQuantity=80, catagory=elektronik_category)
prod6 = Product(name="Tablet", price=3222.99, StockQuantity=70, catagory=elektronik_category)

# Opret produkter relateret til refurbished elektronik
prod7 = Product(name="Refurbished Smartphone", price=499.99, StockQuantity=20, catagory=refurbished_category)
prod8 = Product(name="Refurbished Laptop", price=799.99, StockQuantity=10, catagory=refurbished_category)
prod9 = Product(name="Refurbished Smart TV", price=3500, StockQuantity=15, catagory=refurbished_category)

# Tilføjer kategorier og produkter til databasen
session.add(elektronik_category)  # Tilføj kategorien "Elektronik"
session.add(refurbished_category)  # Tilføj kategorien "Refurbished Elektronik"
session.add_all([prod1, prod2, prod3, prod4, prod5, prod6, prod7, prod8, prod9])  # Tilføj produkterne
session.commit()

# Udskriv alle produkter og deres tilknyttede kategori
for product in session.query(Product).all():
    print(product)
