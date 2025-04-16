from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .service import EmployeesService
from datetime import datetime

employees_view = APIRouter()
templates = Jinja2Templates(directory="app/employees/templates/")
employees_service = EmployeesService()

def format_date(input_date):
    dt = datetime.fromisoformat(input_date)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f") + "+00:00"

@employees_view.get("/employees/select", response_class=HTMLResponse)
async def select_product(request: Request):
    return templates.TemplateResponse("select.html", {"request": request})


@employees_view.get("/employees/report", response_class=HTMLResponse)
async def show_salary_report(
    request: Request,
    start_date: str,
    end_date: str,
    page: int = 1,
):
    formatted_start = format_date(start_date)
    formatted_end = format_date(end_date)

    report = employees_service.get_employee_report(formatted_start, formatted_end, page)
    employees = report["data"]

    metadata = report["metadata"]

    total_pages = metadata["page"] // 10 + 1

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "employees": employees,
            "start_date": start_date,
            "end_date": end_date,
            "current_page": page,
            "total_pages": total_pages
        }
    )
