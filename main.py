from fastapi.middleware.cors import CORSMiddleware
from config.env import env
from fastapi import FastAPI
from app.employees.controller import employees_controller
from app.employees.view import employees_view
from app.orders.controller import order_controller
from app.orders.view import order_view

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin) for origin in env.app_cors_origins.split(",")
    ],
    allow_credentials=True,
    allow_methods=[
        str(method) for method in env.app_cors_methods.split(",")
    ],
    allow_headers=[
        str(header) for header in env.app_cors_headers.split(",")
    ],
)

app.include_router(employees_controller, prefix="/v1/no_injection", tags=["Employees"])
app.include_router(employees_view, tags=["Employees"])
app.include_router(order_controller, prefix="/v1/no_injection", tags=["Orders"])
app.include_router(order_view, tags=["Orders"])
