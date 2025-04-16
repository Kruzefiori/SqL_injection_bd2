from framework.model import ModelGeneric
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.orders.models.order import Orders
else:
    Orders = "Orders"


class Shippers(ModelGeneric):
    __tablename__ = "shippers"
    __table_args__ = (
        PrimaryKeyConstraint("shipperid", name="shippers_pkey"),
        {"schema": "northwind"},
    )

    shipperid: Mapped[int] = mapped_column(Integer, primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(20))
    phone: Mapped[Optional[str]] = mapped_column(String(14))

    orders: Mapped[List["Orders"]] = relationship("Orders", back_populates="shippers")
