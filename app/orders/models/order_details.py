from framework.model import ModelGeneric
from typing import Optional,TYPE_CHECKING
from sqlalchemy import  Integer, ForeignKeyConstraint, Numeric, PrimaryKeyConstraint, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
import decimal
from app.products.model import Products

if TYPE_CHECKING:
    from app.orders.models.order import Orders
else:
    Orders = "Orders"

class OrderDetails(ModelGeneric):
    __tablename__ = 'order_details'
    __table_args__ = (
        ForeignKeyConstraint(['orderid'], ['northwind.orders.orderid'], name='fk_order_details_order'),
        ForeignKeyConstraint(['productid'], ['northwind.products.productid'], name='fk_order_details_product'),
        PrimaryKeyConstraint('orderid', 'productid', name='order_details_pkey'),
        {'schema': 'northwind'}
    )

    orderid: Mapped[int] = mapped_column(Integer, primary_key=True)
    productid: Mapped[int] = mapped_column(Integer, primary_key=True)
    unitprice: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(13, 4))
    quantity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    discount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 4))

    orders: Mapped['Orders'] = relationship('Orders', back_populates='order_details')
    products: Mapped['Products'] = relationship('Products', back_populates='order_details')
