from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0)
    description: str | None = None

    @field_validator("name")
    @classmethod
    def strip_and_validate_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        return stripped


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal
    description: str | None
    image_path: str
    created_at: datetime
