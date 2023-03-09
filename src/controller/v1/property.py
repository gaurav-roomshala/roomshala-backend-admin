from fastapi import APIRouter, Query, Path, Depends
from starlette import status
from fastapi.encoders import jsonable_encoder
from src.utils.helpers.facility_related import get_true_facility, check_if_facility_valid
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers.amenty_related import get_all_amenity, get_true_amenity, check_if_amenity_valid
from src.utils.helpers.db_helpers import find_exist_admin_by_id
from src.utils.helpers.misc import check_documents
from src.utils.helpers.property_related import property_last_entry, find_property_email_id,find_property_mobile_number
from src.utils.logger.logger import logger
from src.models.property_model import Property
from src.utils.helpers.jwt_utils import get_current_user

list_property = APIRouter()

#to create property code check in database of last entry and fetch id and increment that 1


@list_property.post("/property")
async def register_property(property: Property, current_user=Depends(get_current_user)):
    logger.info("======== CREATING PROPERTY =================")
    info = await find_exist_admin_by_id(id=current_user["id"])
    if info["role"] != "SUPER_ADMIN":
        raise CustomExceptionHandler(message="Admin Cannot List Property",
                                     target="UPDATE_STATUS_ADMIN",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False
                                     )
    check_if_email_exist = await find_property_email_id(property_email_id=property.property_email_id)
    if check_if_email_exist:
        raise CustomExceptionHandler(message="Cannot Register Property,Email Exist",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="IF_EMAIL_ALREADY_REGISTERED")

    check_if_number_exist = await find_property_mobile_number(property_mobile_number=property.property_mobile_number)
    if check_if_number_exist:
        raise CustomExceptionHandler(message="Cannot Register Property,Number Exist",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="IF_NUMBER_ALREADY_REGISTERED")

    check_facility = await check_if_facility_valid(facility=property.facilities)
    if not check_facility:
        raise CustomExceptionHandler(code=status.HTTP_400_BAD_REQUEST,
                                     message="Please Check Available Facility Type",
                                     success=False,
                                     target="CHECK_FOR_AVAILABLE_FACILITY"
                                     )
    check_amenity = await check_if_amenity_valid(amenity=property.amenities)
    if not check_amenity:
        raise CustomExceptionHandler(code=status.HTTP_400_BAD_REQUEST,
                                     message="Please Check Available Amenity Type",
                                     success=False,
                                     target="CHECK_FOR_AVAILABLE_AMENITY"
                                     )
    check_docs = check_documents(necessary=dict(property.necessary_documents))
    if not check_docs:
        raise CustomExceptionHandler(code=status.HTTP_400_BAD_REQUEST,
                                     message="Please Check Your Aadhar/Pan Card",
                                     success=False,
                                     target="CHECK_NECESSARY_DOCS"
                                     )
    property.created_by,property.updated_by = current_user["email"],current_user["email"]




@list_property.get("/property")
async def find_property():
    pass
