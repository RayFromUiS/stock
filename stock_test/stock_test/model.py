from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float)

from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # print('uri',get_project_settings().get("SQL_CONNECT_STRING"))
    return create_engine(get_project_settings().get("SQL_CONNECT_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)

class StockTrading(Base):
    __tablename__ = 'stock_trading'
    id = Column(Integer, primary_key=True)
    stock_code = Column(String(24))
    open_date = Column(Date)
    deal_time = Column(DateTime)
    deal_price = Column(Float)
    increment = Column(String(12))
    price_vary = Column(String(12))
    shares = Column(Integer)
    volume = Column(String(12))
    status = Column(String(12))



if __name__ == "__main__":
    db_connect()
