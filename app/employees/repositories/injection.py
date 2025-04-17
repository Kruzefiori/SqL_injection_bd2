from ..model import Employees
from framework.repository import GenericRepositoryInjection


class EmployeesRepositoryInjection(GenericRepositoryInjection):
    def __init__(self):
        super().__init__(Employees)

    def get_employee_report(
        self,
        start_date: str,
        end_date: str,
        page: int = 1,
        page_size: int = 10,
    ):
        self.refresh_cursor()

        try:
            # The query from the ORM should be converted to SQL
            offset = (page - 1) * page_size

            args = {
                "start_date": start_date,
                "end_date": end_date,
                "offset": offset,
                "page_size": page_size,
            }

            query = """
                SELECT e.firstname, e.lastname, e.employeeid, COUNT(o.orderid) AS total_pedidos,
                       SUM(od.unitprice * od.quantity) AS soma_valores_vendidos
                FROM employees e
                JOIN orders o ON o.employeeid = e.employeeid
                JOIN order_details od ON od.orderid = o.orderid
                WHERE o.orderdate BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY e.employeeid
                ORDER BY soma_valores_vendidos DESC
                OFFSET {offset} LIMIT {page_size};
            """.format(**args)

            # print(query)

            self.cursor.execute(query)
            results = self.cursor.fetchall()
            if results:
                column_names = [desc[0] for desc in self.cursor.description]
                return [dict(zip(column_names, row)) for row in results]
            else:
                print("Nenhum resultado encontrado.")

            return []

        except Exception as e:
            raise RuntimeError(
                f"Erro ao buscar informações do funcionários: {e}"
            ) from e
