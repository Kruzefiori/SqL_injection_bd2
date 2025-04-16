from ..models.order import Orders
from framework.repository import GenericRepositoryInjection


class OrdersRepositoryInjection(GenericRepositoryInjection):
    def __init__(self):
        super().__init__(Orders)

    def get_order_report(self, order_id: int):
        session = self._create_a_session()

        try:
            query = """
                SELECT o.orderid, o.orderdate, c.companyname AS customer_name,
                       e.firstname || ' ' || e.lastname AS employee_name,
                       od.productid, od.quantity, od.unitprice
                FROM orders o
                LEFT JOIN customers c ON o.customerid = c.customerid
                LEFT JOIN employees e ON o.employeeid = e.employeeid
                LEFT JOIN orderdetails od ON o.orderid = od.orderid
                WHERE o.orderid = :order_id
            """
            result = session.execute(query, {"order_id": order_id}).fetchall()
            if not result:
                raise ValueError(f"Pedido com ID {order_id} não encontrado")
            order_report = {
                "Número do Pedido": result[0][0],
                "Data do Pedido": result[0][1],
                "Nome do Cliente": result[0][2],
                "Nome do Vendedor": result[0][3],
                "Itens do Pedido": [],
            }
            for row in result:
                product_info = {
                    "Produto": row[4],
                    "Quantidade": row[5],
                    "Preço": row[6],
                }
                order_report["Itens do Pedido"].append(product_info)
            return order_report
        except Exception as e:
            raise RuntimeError(
                f"Erro ao buscar informações do pedido {order_id}: {e}"
            ) from e
        finally:
            session.close()
