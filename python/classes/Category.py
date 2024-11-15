from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

base = declarative_base()

# Definer kategorien "Elektronik" og "Refurbished Elektronik"
class Category(base):
    __tablename__ = 'Categories'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(15), nullable=False)

    # # Relationship tilknytter produkter til kategorien
    # products = relationship("Product", back_populates="catagory")
    

    def __repr__(self):
        return f"<Catagory(CatagoryID={self.CategoryID}, CatagoryName='{self.CategoryName}')>"
