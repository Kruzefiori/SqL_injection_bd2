from framework.model import ModelGeneric
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.products.model import Products
else:
    Products = "Products"


class Suppliers(ModelGeneric):
    __tablename__ = "suppliers"
    __table_args__ = (
        PrimaryKeyConstraint("supplierid", name="supplier_pk"),
        {"schema": "northwind"},
    )

    supplierid: Mapped[int] = mapped_column(Integer, primary_key=True)
    companyname: Mapped[Optional[str]] = mapped_column(String(50))
    contactname: Mapped[Optional[str]] = mapped_column(String(30))
    contacttitle: Mapped[Optional[str]] = mapped_column(String(30))
    address: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(20))
    region: Mapped[Optional[str]] = mapped_column(String(15))
    postalcode: Mapped[Optional[str]] = mapped_column(String(8))
    country: Mapped[Optional[str]] = mapped_column(String(15))
    phone: Mapped[Optional[str]] = mapped_column(String(15))
    fax: Mapped[Optional[str]] = mapped_column(String(15))
    homepage: Mapped[Optional[str]] = mapped_column(String(100))

    products: Mapped[List["Products"]] = relationship(
        "Products", back_populates="suppliers"
    )
