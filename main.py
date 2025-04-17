from fastapi.middleware.cors import CORSMiddleware
from config.env import env
from fastapi import FastAPI
from app.employees.controllers.no_injection import employees_controller
from app.employees.controllers.injection import employees_injection_controller
from app.employees.views.no_injection import employees_view
from app.employees.views.injection import employees_injection_view
from app.orders.controllers.no_injection import order_controller
from app.orders.controllers.injection import order_injection_controller
from app.orders.views.no_injection import order_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in env.app_cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=[str(method) for method in env.app_cors_methods.split(",")],
    allow_headers=[str(header) for header in env.app_cors_headers.split(",")],
)

app.include_router(employees_controller, prefix="/v1/no_injection", tags=["Employees"])
app.include_router(employees_view, tags=["Employees"])
app.include_router(
    employees_injection_view, prefix="/injection", tags=["Employees"]
)
app.include_router(
    employees_injection_controller, prefix="/v1/injection", tags=["Employees"]
)
app.include_router(order_controller, prefix="/v1/no_injection", tags=["Orders"])
app.include_router(order_injection_controller, prefix="/v1/injection", tags=["Orders"])
app.include_router(order_view, tags=["Orders"])
