from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, validator, Field


class ReportRequest(BaseModel):
    start_date: datetime = Field(
        ..., description="Data inicial do relatório (inclusiva)"
    )
    end_date: datetime = Field(..., description="Data final do relatório (inclusiva)")
    page: int = Field(1, gt=0, description="Número da página (a partir de 1)")

    @validator("end_date")
    def validate_date_range(cls, end_date, values):
        if "start_date" in values and end_date < values["start_date"]:
            raise ValueError("A data final deve ser posterior à data inicial.")
        return end_date

    def to_service_params(self) -> Dict[str, Any]:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "page": self.page,
        }

class ReportRequestInjection(BaseModel):
    start_date: str = Field(
        ..., description="Data inicial do relatório (inclusiva)"
    )
    end_date: str = Field(..., description="Data final do relatório (inclusiva)")
    page: int = Field(1, gt=0, description="Número da página (a partir de 1)")

    def to_service_params(self) -> Dict[str, Any]:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "page": self.page,
        }