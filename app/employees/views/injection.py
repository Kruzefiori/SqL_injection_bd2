from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..services.injection import EmployeesServiceInjection

employees_injection_view = APIRouter()
templates = Jinja2Templates(directory="app/employees/templates/")
employees_service = EmployeesServiceInjection()

@employees_injection_view.get("/employees/select", response_class=HTMLResponse)
async def select_product(request: Request):
    return templates.TemplateResponse("select_injection.html", {"request": request})


@employees_injection_view.get("/employees/report", response_class=HTMLResponse)
async def show_salary_report(
    request: Request,
    start_date: str,
    end_date: str,
    page: int = 1,
):
    report = employees_service.get_employee_report(start_date, end_date, page)
    employees = report["data"]

    metadata = report["metadata"]

    total_pages = (metadata["count"] + 9) // 10

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "employees": employees,
            "start_date": start_date,
            "end_date": end_date,
            "current_page": page,
            "total_pages": total_pages,
        },
    )
