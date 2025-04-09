from fastapi.middleware.cors import CORSMiddleware
from config.env import env
from fastapi import FastAPI
from app.orders.controller import order_controller

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

app.include_router(order_controller.router, prefix="/v1/no_injection", tags=["analyze"])
