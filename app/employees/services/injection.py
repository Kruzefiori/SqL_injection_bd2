from framework.service import GenericService
from ..repositories.injection import EmployeesRepositoryInjection
from datetime import datetime
from decimal import Decimal


class EmployeesServiceInjection(GenericService):
    def __init__(self):
        super().__init__(EmployeesRepositoryInjection)

    def get_employee_report(
        self, start_date: datetime, end_date: datetime, page: int = 1
    ):
        raw_data = self.model_repository.get_employee_report(start_date, end_date, page)

        serialized_data = [
            {
                "first_name": row[0],
                "last_name": row[1],
                "employee_id": row[2],
                "total_sales": float(row[3]) if isinstance(row[3], Decimal) else row[3],
            }
            for row in raw_data
        ]

        return {
            "data": serialized_data,
            "metadata": {"count": len(serialized_data), "page": page},
        }
