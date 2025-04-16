from .model import Employees
from framework.repository import GenericRepository
from sqlalchemy import func
from app.orders.models.order import Orders
from app.orders.models.order_details import OrderDetails
from datetime import datetime


class EmployeesRepository(GenericRepository):
    def __init__(self):
            super().__init__(Employees)

    def get_employee_report(self, start_date: datetime, end_date: datetime, page: int = 1, page_size: int = 10):
        session = self._create_a_session()
        try:
            offset = (page - 1) * page_size

            results = session.query(
                    Employees.firstname,
                    Employees.lastname,
                    func.count(Orders.orderid).label('total_pedidos'),
                    func.sum(OrderDetails.unitprice * OrderDetails.quantity).label('soma_valores_vendidos')
                ).join(
                    Orders, Orders.employeeid == Employees.employeeid
                ).join(
                    OrderDetails, OrderDetails.orderid == Orders.orderid
                ).filter(
                    Orders.orderdate >= start_date,
                    Orders.orderdate <= end_date
                ).group_by(
                    Employees.employeeid
                ).order_by(
                    func.sum(OrderDetails.unitprice * OrderDetails.quantity).desc()
                ).offset(offset).limit(page_size).all()

            return results

        except Exception as e:
            session.rollback()
            raise RuntimeError(f"Erro ao buscar informações do funcionários: {e}") from e
        finally:
            session.close()
