from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.orders.services.no_injection import OrderService

order_view = APIRouter()
templates = Jinja2Templates(directory="app/orders/templates/")
order_service = OrderService()


@order_view.get("/orders/select", response_class=HTMLResponse)
async def select_product(request: Request):
    return templates.TemplateResponse("select.html", {"request": request})


@order_view.get("/orders/report", response_class=HTMLResponse)
async def show_orders(
    request: Request, product_id: int, page: int = 1, per_page: int = 5
):
    try:
        all_orders = order_service.get_order_report(product_id)

        orders_data = all_orders.get("data", [])

        metadata = all_orders.get("metadata", {})
        print(metadata)

        if not orders_data and not metadata.get("message"):
            metadata["message"] = (
                f"Nenhum pedido encontrado para o produto ID {product_id}"
            )

        total_orders = len(orders_data)
        total_pages = max(1, (total_orders + per_page - 1) // per_page)
        page = min(page, total_pages)
        start = (page - 1) * per_page
        end = start + per_page
        orders = orders_data[start:end]

        return templates.TemplateResponse(
            "report.html",
            {
                "request": request,
                "orders": orders,
                "product_id": product_id,
                "current_page": page,
                "total_pages": total_pages,
                "metadata": metadata,
            },
        )
    except Exception as e:
        print(f"Error generating order report for product_id {product_id}: {str(e)}")
        raise
