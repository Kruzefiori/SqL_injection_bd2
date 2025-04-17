from ..models.order import Orders
from framework.repository import GenericRepositoryInjection


class OrdersRepositoryInjection(GenericRepositoryInjection):
    def __init__(self):
        super().__init__(Orders)

    def get_order_report(self, order_id: int):
        self.refresh_cursor()
        try:
            query = f"SELECT o.orderid, o.orderdate, c.companyname AS customer_name, e.firstname || ' ' || e.lastname AS employee_name, od.productid, od.quantity, od.unitprice FROM orders o LEFT JOIN customers c ON o.customerid = c.customerid LEFT JOIN employees e ON o.employeeid = e.employeeid LEFT JOIN order_details od ON o.orderid = od.orderid WHERE o.orderid = {order_id};"
            result = self.cursor.execute(query)
            print(query)
            if not result:
                raise ValueError(f"Pedido com ID {order_id} não encontrado")
            
            fetched_result = result.fetchall()
            order_report = {
                "Número do Pedido": fetched_result[0][0],
                "Data do Pedido": fetched_result[0][1],
                "Nome do Cliente": fetched_result[0][2],
                "Nome do Vendedor": fetched_result[0][3],
                "Itens do Pedido": [],
            }
            for row in fetched_result:
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
