from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from classes import Base

# Definer produkter under kategorien "Elektronik"
class Product(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    price = Column(Float, nullable=False)
    StockQuantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('Categories.CategoryID'))

    # # Relationship til kategori
    category = relationship("Category", foreign_keys=[category_id])

    def __repr__(self):
        return (f"<Product(ProductID={self.id}, ProductName='{self.name}', "
                f"Price={self.price}, StockQuantity={self.StockQuantity}, "
                f"Catagory='{self.category_id}')>")
