from model import OrderSchema
from framework.service import GenericService
from repository import OrderRepository


# Bla bla bla, voces entenderam
class OrderService(GenericService):
    def __init__(self):
        super().__init__(OrderRepository, OrderSchema)
