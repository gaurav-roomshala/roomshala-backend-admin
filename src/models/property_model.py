from pydantic import BaseModel,Field, validator

PropertyType = ["Hotel","Bnb"]


class Property(BaseModel):
    property_name:str = Field(...,description="Property Name")
    property_type:str = Field(...,description="Property Type")
    floor_numbers:int = Field(...,description="Number of floors")
    property_description:str = Field(...,description="Description about the property")
    hotel_email_id:str = Field(...,description="Description about the property")
    hotel_mobile_number:str = Field(...,description="")
    complete_address:str = Field(...,description="")
    locality:str
    landmark:str
    pincode:str
    city:str
    state:str
    longitude:str
    latitude:str