from model import OrderDB
from framework.repository import GenericRepository


# Se quiser da sobrecarga ou extender eh aqui
class OrderRepository(GenericRepository):
    def __init__(self, session):
        def __init__(self):
                super().__init__(OrderDB)
