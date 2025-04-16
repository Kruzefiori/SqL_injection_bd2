from .model import Orders
from framework.repository import GenericRepository

class OrderRepository(GenericRepository):
    def __init__(self, session):
        def __init__(self):
                super().__init__(Orders)
