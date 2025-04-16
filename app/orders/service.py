from framework.service import GenericService
from .repository import OrderRepository



class OrderService(GenericService):
    def __init__(self):
        super().__init__(OrderRepository)

    def get_order_report(self, product_id: int):
        answer = self.model_repository.get_order_report(product_id)

        if not answer or 'Itens do Pedido' not in answer:
            return {"data": [], "metadata": {"message": "Product not found or no items in the order"}}

        report_data = []
        for item in answer['Itens do Pedido']:
            report_item = {
                "order_id": answer['Número do Pedido'],
                "date": answer['Data do Pedido'].strftime("%Y-%m-%d"),
                "customer_name": answer['Nome do Cliente'],
                "salesperson_name": answer['Nome do Vendedor'],
                "item_product": item['Produto'],
                "quantity": item['Quantidade'],
                "price": float(item['Preço']),
                "total": float(item['Preço']) * item['Quantidade']
            }
            report_data.append(report_item)

        return {
            "data": report_data,
            "metadata": {
                "total": len(report_data),
                "page": 1,
                "product_id": product_id
            }
        }
