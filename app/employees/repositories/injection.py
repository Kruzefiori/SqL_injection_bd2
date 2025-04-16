from ..model import Employees
from framework.repository import GenericRepositoryInjection
from datetime import datetime


class EmployeesRepositoryInjection(GenericRepositoryInjection):
    def __init__(self):
        super().__init__(Employees)

    def get_employee_report(
        self,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
        page_size: int = 10,
    ):
        session = self._create_a_session()

        try:
            # The query from the ORM should be converted to SQL
            offset = (page - 1) * page_size

            query = """
                SELECT e.firstname, e.lastname, COUNT(o.orderid) AS total_pedidos,
                       SUM(od.unitprice * od.quantity) AS soma_valores_vendidos
                FROM employees e
                JOIN orders o ON o.employeeid = e.employeeid
                JOIN orderdetails od ON od.orderid = o.orderid
                WHERE o.orderdate BETWEEN :start_date AND :end_date
                GROUP BY e.employeeid
                ORDER BY soma_valores_vendidos DESC
                OFFSET :offset LIMIT :page_size;
            """
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "offset": offset,
                "page_size": page_size,
            }

            session.execute(query, params)
            results = session.fetchall()
            return results

        except Exception as e:
            raise RuntimeError(
                f"Erro ao buscar informações do funcionários: {e}"
            ) from e
        finally:
            session.close()
