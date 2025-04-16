from typing import Dict, Any, List
from pydantic import BaseModel


class EmployeeReportItem(BaseModel):
    first_name: str
    last_name: str
    employee_id: int
    total_sales: float


class ReportResponse(BaseModel):
    data: Dict[str, List[EmployeeReportItem]]
    metadata: Dict[str, Any]

    @classmethod
    def from_service_data(cls, raw_data: Dict[str, Any]) -> "ReportResponse":
        return cls(
            data={"employees": raw_data.get("data", [])},
            metadata=raw_data.get("metadata", {}),
        )
