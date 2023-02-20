from pydantic import BaseModel, Field, validator
from datetime import datetime


class Amenties(BaseModel):
    name: str = Field(..., description="Amenty Name")
    is_active: bool = Field(default=True, description="status")
    created_on: datetime = Field(default=None)

    @validator("name")
    def validate_name(cls, value):
        value = value.capitalize()
        return value


class AmenityUpdate(BaseModel):
    is_active: bool = Field(default=False, description="status")