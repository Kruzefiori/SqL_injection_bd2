from framework.model import ModelGeneric
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.orders.models.order import Orders
else:
    Orders = "Orders"


class Customers(ModelGeneric):
    __tablename__ = "customers"
    __table_args__ = (
        PrimaryKeyConstraint("customerid", name="customers_pkey"),
        {"schema": "northwind"},
    )

    customerid: Mapped[str] = mapped_column(String(5), primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(50))
    contactname: Mapped[Optional[str]] = mapped_column(String(30))
    contacttitle: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postalcode: Mapped[Optional[str]] = mapped_column(String(9))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(17))
    fax: Mapped[Optional[str]] = mapped_column(String(17))

    orders: Mapped[List["Orders"]] = relationship("Orders", back_populates="customers")
