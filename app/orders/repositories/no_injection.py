from ..models.order import Orders
from ..models.order_details import OrderDetails
from framework.repository import GenericRepository
from sqlalchemy.orm import joinedload
from typing import override
from sqlalchemy.future import select
from datetime import datetime
from decimal import Decimal
from app.customers.model import Customers
from app.employees.model import Employees
from app.products.model import Products
import math
import random

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

    @override
    def create(self, item):
        session = self._create_a_session()

        cliente_nome = item["cliente_nome"]
        vendedor_nome = item["vendedor_nome"]
        pedido_data = datetime.strptime(item["pedido_data"], "%Y-%m-%d")
        itens = item["itens"]

        cliente = session.execute(
            select(Customers).where(Customers.contactname == cliente_nome)
        ).scalars().first()
        if not cliente:
            raise ValueError(f"Cliente '{cliente_nome}' não encontrado.")

        vendedor = session.execute(
            select(Employees).where(Employees.firstname == vendedor_nome)
        ).scalars().first()
        if not vendedor:
            raise ValueError(f"Vendedor '{vendedor_nome}' não encontrado.")

        novo_pedido = Orders(
            customerid=cliente.customerid,
            employeeid=vendedor.employeeid,
            orderdate=pedido_data,
            orderid=420+math.floor(random.random() * 1000)
        )
        session.add(novo_pedido)
        session.commit()

        for item_detalhe in itens:
            produto = session.execute(
                select(Products).where(Products.productname == item_detalhe["nome"])
            ).scalars().first()
            if not produto:
                raise ValueError(f"Produto '{item_detalhe['nome']}' não encontrado.")

            detalhe = OrderDetails(
                orderid=novo_pedido.orderid,
                productid=produto.productid,
                unitprice=Decimal(str(item_detalhe["preco"])),
                quantity=item_detalhe["quantidade"],
                discount=0
            )
            session.add(detalhe)

        session.commit()
        return novo_pedido.orderid
