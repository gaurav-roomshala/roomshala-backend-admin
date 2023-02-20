from fastapi import APIRouter, Query, Path, Depends
from starlette import status
from fastapi.encoders import jsonable_encoder


list_property = APIRouter()


@list_property.post("/property")
async def register_property():
    #user based access , can only be created by super roomshala owner
    #generate property code by id
    #check if facility exist
    #check if amenities exist
    #map them to another table
    #map with property user table
    pass