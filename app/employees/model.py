from typing import Optional
from sqlalchemy import DateTime, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from infrastructure.databases.SQL.pg_alchemy import SqlDB
import datetime

Base = SqlDB().get_base()

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        PrimaryKeyConstraint('employeeid', name='employees_pkey'),
        {'schema': 'northwind'}
    )

    employeeid: Mapped[int] = mapped_column(Integer, primary_key=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(10))
    firstname: Mapped[Optional[str]] = mapped_column(String(10))
    title: Mapped[Optional[str]] = mapped_column(String(25))
    titleofcourtesy: Mapped[Optional[str]] = mapped_column(String(5))
    birthdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    hiredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(2))
    postalcode: Mapped[Optional[str]] = mapped_column(String(9))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    homephone: Mapped[Optional[str]] = mapped_column(String(14))
    extension: Mapped[Optional[str]] = mapped_column(String(4))
    reportsto: Mapped[Optional[int]] = mapped_column(Integer)
    notes: Mapped[Optional[str]] = mapped_column(Text)