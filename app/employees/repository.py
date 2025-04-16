from .model import Employee
from framework.repository import GenericRepository


# Se quiser da sobrecarga ou extender eh aqui
class EmployeeRepository(GenericRepository):
    def __init__(self, session):
        def __init__(self):
                super().__init__(Employee)
