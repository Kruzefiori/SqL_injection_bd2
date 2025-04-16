from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..services.no_injection import EmployeesService

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
    start_datetime = datetime.fromisoformat(start_date)
    end_datetime = datetime.fromisoformat(end_date)

    report = employees_service.get_employee_report(start_datetime, end_datetime, page)
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
