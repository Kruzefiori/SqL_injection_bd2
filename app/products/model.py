from framework.model import ModelGeneric
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import (
    Integer,
    ForeignKeyConstraint,
    Numeric,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import decimal
from app.categories.model import Categories
from app.suppliers.model import Suppliers

if TYPE_CHECKING:
    from app.orders.models.order import Orders
    from app.orders.models.order_details import OrderDetails

else:
    Orders = "Orders"


class Products(ModelGeneric):
    __tablename__ = "products"
    __table_args__ = (
        ForeignKeyConstraint(
            ["categoryid"], ["northwind.categories.categoryid"], name="fk_category"
        ),
        ForeignKeyConstraint(
            ["supplierid"], ["northwind.suppliers.supplierid"], name="fk_supplier"
        ),
        PrimaryKeyConstraint("productid", name="products_pkey"),
        {"schema": "northwind"},
    )

    productid: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplierid: Mapped[int] = mapped_column(Integer)
    categoryid: Mapped[int] = mapped_column(Integer)
    productname: Mapped[Optional[str]] = mapped_column(String(35))
    quantityperunit: Mapped[Optional[str]] = mapped_column(String(20))
    unitprice: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(13, 4))
    unitsinstock: Mapped[Optional[int]] = mapped_column(SmallInteger)
    unitsonorder: Mapped[Optional[int]] = mapped_column(SmallInteger)
    reorderlevel: Mapped[Optional[int]] = mapped_column(SmallInteger)
    discontinued: Mapped[Optional[str]] = mapped_column(String(1))

    categories: Mapped["Categories"] = relationship(
        "Categories", back_populates="products"
    )
    suppliers: Mapped["Suppliers"] = relationship(
        "Suppliers", back_populates="products"
    )
    order_details: Mapped[List["OrderDetails"]] = relationship(
        "OrderDetails", back_populates="products"
    )
