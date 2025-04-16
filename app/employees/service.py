from .model import Employee
from framework.service import GenericService
from repository import EmployeeRepository


# Bla bla bla, voces entenderam
class EmployeeService(GenericService):
    def __init__(self):
        super().__init__(EmployeeRepository, Employee)
