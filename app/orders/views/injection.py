from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.orders.services.injection import OrderServiceInjection
import re

order_view_injection = APIRouter()
templates = Jinja2Templates(directory="app/orders/templates/")
order_service = OrderServiceInjection()

@order_view_injection.get("/orders/select", response_class=HTMLResponse)
async def select_product(request: Request):
    return templates.TemplateResponse("select.html", {"request": request})


@order_view_injection.get("/orders/report", response_class=HTMLResponse)
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

@order_view_injection.get("/orders", response_class=HTMLResponse)
async def show_order_form(request: Request):
    return templates.TemplateResponse("insert_injection.html", {"request": request})


@order_view_injection.post("/orders")
async def save_order(
    request: Request,
    cliente_nome: str = Form(...),
    vendedor_nome: str = Form(...),
    pedido_numero: str = Form(...),
    pedido_data: str = Form(...),
):
    form = await request.form()
    raw_itens = []

    index = 0
    for key, value in form.items():
        if key.startswith("itens["):
            match = re.match(r"itens\[\$\{itemIndex\}\]\[(.*?)\]", key)
            if match:
                field = match.group(1).lower()
                if field == "nome":
                    raw_itens.append({})
                    raw_itens[index]["nome"] = value.strip()
                elif field == "quantidade":
                    raw_itens[index]["quantidade"] = str(value)
                elif field == "preco":
                    raw_itens[index]["preco"] = float(value)
                    index += 1

    order_service.create(
        {
            "cliente_nome": cliente_nome,
            "vendedor_nome": vendedor_nome,
            "pedido_numero": pedido_numero,
            "pedido_data": pedido_data,
            "itens": raw_itens,
        }
    )
    return RedirectResponse(url="/orders", status_code=303)
