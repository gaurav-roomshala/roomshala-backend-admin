from pydantic import BaseModel, Field


class HotelAdmin(BaseModel):
    first_name:str
    last_name:str
    email_id:str
    contact_number:str
    role:str
    property_id:int
