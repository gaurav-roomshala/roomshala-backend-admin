import re
from pydantic import BaseModel, Field, validator
from datetime import datetime
from starlette import status
from src.constants.utilities import PHONE_REGEX, EMAIL_REGEX
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from typing import List, Dict

PropertyType = ["Hotel", "Bnb"]


class NecessaryDocs(BaseModel):
    aadhar: str = Field(..., description="")
    pancard: str = Field(..., description="")


class PropertyDocs(BaseModel):
    property_images: List[Dict] = Field(..., description="")
    legal_papers: List[Dict] = Field(..., description="")


class Property(BaseModel):
    property_name: str = Field(..., description="Property Name")
    property_type: str = Field(..., description="Property Type")
    floor_numbers: int = Field(..., description="Number of floors")
    property_description: str = Field(..., description="Description about the property")
    property_email_id: str = Field(..., description="Description about the property")
    property_mobile_number: str = Field(..., description="")
    complete_address: str = Field(..., description="")
    locality: str
    landmark: str
    pincode: str
    city: str
    state: str
    longitude: str
    latitude: str
    necessary_documents: NecessaryDocs
    facilities: List[int] = Field(..., description="Facilities")
    amenities: List[int] = Field(..., description="")
    property_docs: PropertyDocs
    is_active: bool = Field(default=False)
    created_on: datetime
    created_by: str
    updated_on: datetime
    updated_by: str

    @validator("state")
    @classmethod
    def state_lower(cls, value):
        return value.lower()

    @validator("city")
    @classmethod
    def city_lower(cls, value):
        return value.lower()

    @validator("locality")
    @classmethod
    def locality_lower(cls, value):
        return value.lower()

    @validator("facilities")
    @classmethod
    def check_if_facility_unique(cls, value):
        flag = len(set(value)) == len(value)
        if not flag:
            raise CustomExceptionHandler(message="Duplicate Entry In Facility",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target=""
                                         )
        return value

    @validator("amenities")
    @classmethod
    def check_if_amenity_unique(cls, value):
        flag = len(set(value)) == len(value)
        if not flag:
            raise CustomExceptionHandler(message="Duplicate Entry In Amenities",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target=""

                                         )
        return value

    @validator("property_type")
    @classmethod
    def check_available_property_types(cls, value):
        if value not in PropertyType:
            raise CustomExceptionHandler(
                message="Please Check The Property Type, Available Types {}".format(PropertyType),
                code=status.HTTP_400_BAD_REQUEST,
                target="",
                success=False
            )
        return value

    @validator("property_email_id")
    @classmethod
    def check_email(cls, value):
        pattern = re.compile(EMAIL_REGEX)
        if not pattern.match(value):
            raise CustomExceptionHandler(message="Please enter a valid email",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target="",
                                         success=False
                                         )
        return value

    @validator("property_mobile_number")
    @classmethod
    def check_phone_number_regex(cls, value):
        pattern = re.compile(PHONE_REGEX)
        if not pattern.match(value):
            raise CustomExceptionHandler(message="Please enter a valid phone number",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target="",
                                         success=False
                                         )
        return value
