from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

base = declarative_base()

class Catagory(base):
    __tablename__ = 'Catagory'

    id = Column(Integer, primary_key=True)
    name = Column(String)
