from fastapi import APIRouter, Query, Path, Depends
from starlette import status
from fastapi.encoders import jsonable_encoder


list_property = APIRouter()


@list_property.post("/property")
async def register_property():
    pass

