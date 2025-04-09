from fastapi import APIRouter
from model import OrderSchema
from service import OrderService
from framework.controller import GenericRouter

router = APIRouter()
user_service = OrderService()

router.tags = ["orders"]

order_controller = GenericRouter(
    model_service=OrderService,
    model_schema=OrderSchema,
    class_name="orders",
    router=router
)
