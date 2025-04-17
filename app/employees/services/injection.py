from framework.service import GenericService
from ..repositories.injection import EmployeesRepositoryInjection


class EmployeesServiceInjection(GenericService):
    def __init__(self):
        super().__init__(EmployeesRepositoryInjection)

    def get_employee_report(
        self, start_date: str, end_date: str, page: int = 1
    ):
        raw_data = self.model_repository.get_employee_report(start_date, end_date, page)

        serialized_data = [
            {
                "first_name": row['firstname'],
                "last_name": row['lastname'],
                "employee_id": row['employeeid'],
                "sales": {
                    "total": row['soma_valores_vendidos'],
                    "count": row['total_pedidos']
                },
            }
            for row in raw_data
        ]

        return {
            "data": serialized_data,
            "metadata": {"count": len(serialized_data), "page": page},
        }
