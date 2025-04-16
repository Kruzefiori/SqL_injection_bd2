from ..models.order import Orders
from ..models.order_details import OrderDetails
from framework.repository import GenericRepository
from sqlalchemy.orm import joinedload


class OrderRepository(GenericRepository):
    def __init__(self):
        super().__init__(Orders)

    def get_order_report(self, order_id: int):
        session = self._create_a_session()
        try:
            order = (
                session.query(Orders)
                .filter(Orders.orderid == order_id)
                .options(
                    joinedload(Orders.customers),
                    joinedload(Orders.employees),
                    joinedload(Orders.order_details).joinedload(OrderDetails.products),
                )
                .first()
            )

            if not order:
                raise ValueError(f"Pedido com ID {order_id} não encontrado")

            order_report = {
                "Número do Pedido": order.orderid,
                "Data do Pedido": order.orderdate,
                "Nome do Cliente": order.customers.companyname
                if order.customers
                else "N/A",
                "Nome do Vendedor": f"{order.employees.firstname} {order.employees.lastname}"
                if order.employees
                else "N/A",
                "Itens do Pedido": [],
            }

            for item in order.order_details:
                product_info = {
                    "Produto": item.products.productname if item.products else "N/A",
                    "Quantidade": item.quantity,
                    "Preço": item.unitprice,
                }
                order_report["Itens do Pedido"].append(product_info)

            return order_report
        except Exception as e:
            session.rollback()
            raise RuntimeError(
                f"Erro ao buscar informações do pedido {order_id}: {e}"
            ) from e
        finally:
            session.close()
