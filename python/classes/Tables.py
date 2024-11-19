from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKeyConstraint
from sqlalchemy.sql.schema import MetaData
def create_tables(metadata : MetaData):
    categories = Table(
        'Categories', metadata,
        Column("CategoryID", Integer, primary_key=True, autoincrement=True),
        Column("CategoryName", String(15), nullable=False)
    )
    
    products = Table(
        'Products', metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("category_id", Integer, nullable=False),
        Column("name", String(15), nullable=False),
        Column("price", Float, nullable=False),
        Column("StockQuantity", Integer, nullable=False),
        ForeignKeyConstraint(["category_id"],["Categories.CategoryID"])
    )

    return metadata
