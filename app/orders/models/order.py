from framework.model import ModelGeneric
from typing import List, Optional
from sqlalchemy import (
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from datetime import datetime
from app.customers.model import Customers
from app.employees.model import Employees
from app.shippers.model import Shippers
from .order_details import OrderDetails


class Orders(ModelGeneric):
    __tablename__ = "orders"
    __table_args__ = (
        ForeignKeyConstraint(
            ["customerid"], ["northwind.customers.customerid"], name="fk_customer"
        ),
        ForeignKeyConstraint(
            ["employeeid"], ["northwind.employees.employeeid"], name="fk_employee"
        ),
        ForeignKeyConstraint(
            ["shipperid"], ["northwind.shippers.shipperid"], name="fk_shipper"
        ),
        PrimaryKeyConstraint("orderid", name="orders_pkey"),
        {"schema": "northwind"},
    )

    orderid: Mapped[int] = mapped_column(Integer, primary_key=True)
    customerid: Mapped[str] = mapped_column(String(5))
    employeeid: Mapped[int] = mapped_column(Integer)
    orderdate: Mapped[Optional[datetime]] = mapped_column(DateTime)
    requireddate: Mapped[Optional[datetime]] = mapped_column(DateTime)
    shippeddate: Mapped[Optional[datetime]] = mapped_column(DateTime)
    freight: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4))
    shipname: Mapped[Optional[str]] = mapped_column(String(35))
    shipaddress: Mapped[Optional[str]] = mapped_column(String(50))
    shipcity: Mapped[Optional[str]] = mapped_column(String(15))
    shipregion: Mapped[Optional[str]] = mapped_column(String(15))
    shippostalcode: Mapped[Optional[str]] = mapped_column(String(9))
    shipcountry: Mapped[Optional[str]] = mapped_column(String(15))
    shipperid: Mapped[Optional[int]] = mapped_column(Integer)

    customers: Mapped["Customers"] = relationship("Customers", back_populates="orders")
    employees: Mapped["Employees"] = relationship("Employees", back_populates="orders")
    shippers: Mapped[Optional["Shippers"]] = relationship(
        "Shippers", back_populates="orders"
    )
    order_details: Mapped[List["OrderDetails"]] = relationship(
        "OrderDetails", back_populates="orders"
    )
