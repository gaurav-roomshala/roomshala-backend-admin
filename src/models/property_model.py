from pydantic import BaseModel, Field, validator
from datetime import datetime

PropertyType = ["Hotel", "Bnb"]


class NecessaryDocs:
    aadhar: str = Field(..., description="")
    pancard: str = Field(..., description="")


class PropertyDocs:
    property_images: list = Field(..., description="")
    legal_papers: list = Field(..., description="")


class Property(BaseModel):
    property_name: str = Field(..., description="Property Name")
    property_type: str = Field(..., description="Property Type")
    floor_numbers: int = Field(..., description="Number of floors")
    property_description: str = Field(..., description="Description about the property")
    hotel_email_id: str = Field(..., description="Description about the property")
    hotel_mobile_number: str = Field(..., description="")
    complete_address: str = Field(..., description="")
    locality: str
    landmark: str
    pincode: str
    city: str
    state: str
    longitude: str
    latitude: str
    necessary_documents: NecessaryDocs = Field(..., description="Documents")
    facilities: list = Field(..., description="Facilities")
    amenities: list = Field(..., description="")
    property_docs = PropertyDocs
    created_on:datetime
    created_by:str
    updated_on:datetime
    updated_by:str
