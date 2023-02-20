from pydantic import BaseModel, Field, validator
from datetime import datetime
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from starlette import status

FACILITIES_TYPE = ["ROOM_SERVICE", "TERRACE", "KEY_CARD_ACCESS",
                   "24_HOUR_FRONT_DESK", "NON_SMOKING_ROOM",
                   "ADULTS_ONLY", "FITNESS_CENTER", "COUPLE_FRIENDLY",
                   "SOUNDPROOF_ROOMS", "SWIMMING_POOL", "KEY_ACCESS", "PETS_ALLOWED"
                   ]


class FacilityUpdate(BaseModel):
    is_active: bool = Field(default=False, description="status")


class Facilities(BaseModel):
    name: str = Field(..., description="Facility Name")
    is_active: bool = Field(default=True, description="status")
    created_on: datetime = Field(default=None)

    @validator("name")
    def validate_name(cls, value):
        if value not in FACILITIES_TYPE:
            raise CustomExceptionHandler(message="Please Provide Valid Facility",
                                         target="CHECK_FACILITY_NAME",
                                         code=status.HTTP_404_NOT_FOUND,
                                         success=False)
        return value
