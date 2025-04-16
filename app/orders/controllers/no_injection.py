from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from framework.controller import create_generic_router
from ..models.order import Orders
from ..services.no_injection import OrderService
from ..dtos.product_report_request import ProductReportRequest
from ..dtos.product_report_response import ProductReportResponse

order_service = OrderService()

order_controller = create_generic_router(
    service=order_service, schema=Orders, class_name="orders"
)


@order_controller.post(
    "/report/{product_id}",
    response_model=ProductReportResponse,
    description="Gera um relatório detalhado dos pedidos de um produto específico",
    response_description="Relatório do pedido do produto com metadados",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Relatório do produto gerado com sucesso"},
        400: {"description": "ID do produto inválido"},
        404: {"description": "Produto não encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
)
async def generate_report(product_id: int) -> JSONResponse:
    try:
        request = ProductReportRequest(product_id=product_id)
        service_params = request.to_service_params()

        report_data = order_service.get_order_report(**service_params)

        if not report_data or not report_data.get("data"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado ou sem dados disponíveis",
            )

        response = ProductReportResponse.from_service_data(
            product_id=request.product_id, raw_data=report_data
        )

        return JSONResponse(
            content=jsonable_encoder(response), status_code=status.HTTP_200_OK
        )

    except ValueError as e:
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST
        )

    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)

    except Exception as e:
        print(f"Erro interno do servidor: {e}")
        return JSONResponse(
            content={"error": "Erro interno do servidor"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
