from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder
from framework.controller import create_generic_router
from ..dtos.report_request import ReportRequest
from ..dtos.report_response import ReportResponse
from ..model import Employees
from ..services.no_injection import EmployeesService

employees_service = EmployeesService()

employees_controller = create_generic_router(
    service=employees_service, schema=Employees, class_name="employees"
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
        500: {"description": "Erro interno do servidor"},
    },
)
async def generate_report(request_data: ReportRequest) -> JSONResponse:
    try:
        service_params = request_data.to_service_params()

        report_data = employees_service.get_employee_report(**service_params)

        print(report_data)

        response = ReportResponse.from_service_data(report_data)

        return JSONResponse(
            content=jsonable_encoder(response), status_code=status.HTTP_200_OK
        )

    except ValueError as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return JSONResponse(
            content={"error": "Erro interno ao gerar relatório"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
