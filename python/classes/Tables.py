from sqlalchemy import Table, Column, Float, Integer, String, MetaData
from sqlalchemy.sql.schema import MetaData
def create_tables(metadata : MetaData):
    products = Table(
        'Products', metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(15), nullable=False),
        Column("price", Float, nullable=False),
        Column("StockQuantity", Integer, nullable=False)
    )

    categories = Table(
        'Categories', metadata,
        Column("CategoryId", Integer, primary_key=True, autoincrement=True),
        Column("CategoryName", String(15), nullable=False)
    )

    return metadata
