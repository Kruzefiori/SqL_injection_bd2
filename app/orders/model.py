from pydantic import BaseModel
from typing import Optional
from sqlalchemy import DateTime, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from infrastructure.databases.SQL.pg_alchemy import SqlDB
import datetime
import decimal

Base = SqlDB().get_base()

class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('orderid', name='orders_pkey'),
        {'schema': 'northwind'}
    )

    orderid: Mapped[int] = mapped_column(Integer, primary_key=True)
    customerid: Mapped[str] = mapped_column(String(5))
    employeeid: Mapped[int] = mapped_column(Integer)
    orderdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    requireddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shippeddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    freight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 4))
    shipname: Mapped[Optional[str]] = mapped_column(String(35))
    shipaddress: Mapped[Optional[str]] = mapped_column(String(50))
    shipcity: Mapped[Optional[str]] = mapped_column(String(15))
    shipregion: Mapped[Optional[str]] = mapped_column(String(15))
    shippostalcode: Mapped[Optional[str]] = mapped_column(String(9))
    shipcountry: Mapped[Optional[str]] = mapped_column(String(15))
    shipperid: Mapped[Optional[int]] = mapped_column(Integer)
