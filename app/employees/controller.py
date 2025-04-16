from fastapi.responses import JSONResponse
from framework.controller import create_generic_router
from .model import Employees
from .service import EmployeesService
from fastapi import status
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel, validator, Field

employees_service = EmployeesService()

employees_controller = create_generic_router(
    service=employees_service,
    schema=Employees,
    class_name="employees"
)

class ReportRequest(BaseModel):
    start_date: datetime = Field(..., description="Data inicial do relatório (inclusiva)")
    end_date: datetime = Field(..., description="Data final do relatório (inclusiva)")
    page: int = Field(1, gt=0, description="Número da página (a partir de 1)")

    @validator('end_date')
    def validate_date_range(cls, end_date, values):
        if 'start_date' in values and end_date < values['start_date']:
            raise ValueError("A data final deve ser posterior à data inicial.")
        return end_date

    def to_service_params(self) -> Dict[str, Any]:
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'page': self.page
        }

class EmployeeReportItem(BaseModel):
    first_name: str
    last_name: str
    employee_id: int
    total_sales: float

class ReportResponse(BaseModel):
    data: Dict[str, List[EmployeeReportItem]]
    metadata: Dict[str, Any]

    @classmethod
    def from_service_data(cls, raw_data: Dict[str, Any]) -> 'ReportResponse':
        return cls(
            data={"employees": raw_data.get("data", [])},
            metadata=raw_data.get("metadata", {})
        )

@employees_controller.post(
    "/report/",
    response_model=ReportResponse,
    description="Gera um relatório de funcionários dentro de um intervalo de datas",
    response_description="Relatório em JSON contendo dados de funcionários e metadados",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Relatório gerado com sucesso"},
        400: {"description": "Parâmetros inválidos"},
        422: {"description": "Erro de validação"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def generate_report(request_data: ReportRequest) -> JSONResponse:
    try:
        service_params = request_data.to_service_params()

        report_data = employees_service.get_employee_report(**service_params)

        print(report_data)

        response = ReportResponse.from_service_data(report_data)

        return JSONResponse(
            content=jsonable_encoder(response),
            status_code=status.HTTP_200_OK
        )

    except ValueError as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return JSONResponse(
            content={"error": "Erro interno ao gerar relatório"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
