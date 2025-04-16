from framework.model import ModelGeneric
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.products.model import Products
else:
    Products = "Products"

class Categories(ModelGeneric):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('categoryid', name='categories_pkey'),
        {'schema': 'northwind'}
    )

    categoryid: Mapped[int] = mapped_column(Integer, primary_key=True)
    categoryname: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(100))

    products: Mapped[List['Products']] = relationship('Products', back_populates='categories')

