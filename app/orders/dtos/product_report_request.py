from pydantic import BaseModel, Field, validator
from typing import Dict, Any


class ProductReportRequest(BaseModel):
    product_id: int = Field(
        ..., gt=0, description="ID da ordem para gerar o relatório"
    )

    @validator("product_id")
    def validate_product_id(cls, value):
        if value <= 0:
            raise ValueError("O ID da ordem deve ser positivo")
        return value

    def to_service_params(self) -> Dict[str, Any]:
        return {"product_id": self.product_id}
