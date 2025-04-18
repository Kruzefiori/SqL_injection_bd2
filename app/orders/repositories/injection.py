from ..models.order import Orders
from framework.repository import GenericRepositoryInjection
import math
import random

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
    
    def create(self, item):
        self.refresh_cursor()

        cliente_nome = item["cliente_nome"]
        vendedor_nome = item["vendedor_nome"]
        pedido_data = item["pedido_data"]
        itens = item["itens"]

        try:
            cliente_query = f"SELECT customerid FROM customers WHERE contactname = '{cliente_nome}'"
            self.cursor.execute(cliente_query)
            cliente = self.cursor.fetchone()
            if not cliente:
                raise ValueError(f"Cliente '{cliente_nome}' não encontrado.")
            customerid = cliente[0]

            vendedor_query = f"SELECT employeeid FROM employees WHERE firstname = '{vendedor_nome}'"
            self.cursor.execute(vendedor_query)
            vendedor = self.cursor.fetchone()
            if not vendedor:
                raise ValueError(f"Vendedor '{vendedor_nome}' não encontrado.")
            employeeid = vendedor[0]

            orderid = 420 + int(random.random() * 1000)
            pedido_query = f"""
                INSERT INTO orders (orderid, customerid, employeeid, orderdate)
                VALUES ({orderid}, '{customerid}', '{employeeid}', '{pedido_data}')
            """
            self.cursor.execute(pedido_query)

            # Inserir detalhes dos pedidos
            for item_detalhe in itens:
                produto_query = f"SELECT productid FROM products WHERE productname = '{item_detalhe['nome']}'"
                self.cursor.execute(produto_query)
                produto = self.cursor.fetchone()
                if not produto:
                    raise ValueError(f"Produto '{item_detalhe['nome']}' não encontrado.")
                productid = produto[0]

                detalhe_query = f"""
                    INSERT INTO order_details (orderid, productid, unitprice, quantity, discount)
                    VALUES ({orderid}, '{productid}', {item_detalhe['preco']}, {item_detalhe['quantidade']}, 0)
                """
                print(detalhe_query)
                self.cursor.execute(detalhe_query)

            print(f"Pedido {orderid} criado com sucesso.")
            # Faz o commit
            self.connection.commit()
            return orderid

        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Erro ao criar o pedido: {e}") from e