from pydantic import BaseModel, Field
from typing import Dict, Any, List

class OrderReportItem(BaseModel):
    order_id: int
    date: str
    customer_name: str
    salesperson_name: str
    item_product: str
    quantity: int
    price: float
    total: float

class ProductReportResponse(BaseModel):
    product_id: int
    report_data: List[OrderReportItem]
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_service_data(cls, product_id: int, raw_data: Dict[str, Any]) -> 'ProductReportResponse':
        return cls(
            product_id=product_id,
            report_data=raw_data.get('data', []),
            metadata=raw_data.get('metadata', {})
        )
