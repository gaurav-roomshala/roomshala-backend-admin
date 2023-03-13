import json
from fastapi import APIRouter, Query, Path, Depends
from starlette import status
from fastapi.encoders import jsonable_encoder
from src.constants.field import TRUE, FALSE
from src.utils.helpers.facility_related import get_true_facility, check_if_facility_valid, get_facility_of_property
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers.amenty_related import get_all_amenity, get_true_amenity, check_if_amenity_valid, \
    get_amenity_of_property
from src.utils.helpers.db_helpers import find_exist_admin_by_id
from src.utils.helpers.misc import check_documents, modify_docs
from src.utils.helpers.property_related import property_last_entry, find_property_email_id, find_property_mobile_number, \
    list_new_property, find_particular_property_information, get_active_property, get_all_property, \
    get_non_active_property
from src.utils.logger.logger import logger
from src.models.property_model import Property
from src.utils.helpers.jwt_utils import get_current_user
from src.utils.response.data_response import ResponseModel

list_property = APIRouter()


# to create property code check in database of last entry and fetch id and increment that 1


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
    property.created_by, property.updated_by = current_user["email"], current_user["email"]
    necessary_docs = modify_docs(docs=dict(property.necessary_documents))
    property_docs = modify_docs(docs=dict(property.property_docs))
    property.necessary_documents = necessary_docs
    property.property_docs = property_docs
    success = await list_new_property(property=property, code="RS-11")
    if success[0]:
        property_information = await find_particular_property_information(id=success[1])
        property_information = dict(property_information)
        info = {"facility": await get_facility_of_property(property_id=success[1]),
                "amenity": await get_amenity_of_property(property_id=success[1])
                }
        property_information.update(info)
        # print(results)
        return ResponseModel(message="Successfully Created Property",
                             code=status.HTTP_201_CREATED,
                             data=property_information,
                             success=True
                             )
    else:
        raise CustomExceptionHandler(message="Something Went Wrong In Creating Property",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="",
                                     success=False
                                     )


@list_property.get("/property")
async def find_property(active_state: str = Query(None, description="to get which state amenity"),
                        state: str = Query(None, description="")):
    if active_state == TRUE:
        if state is None:
            raise CustomExceptionHandler(message="Please Provide State",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target=""
                                         )
        return ResponseModel(message="True State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data=await get_active_property(state=state.lower())
                             ).response()

    elif active_state == FALSE:
        if state is None:
            raise CustomExceptionHandler(message="Please Provide State",
                                         success=False,
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target=""
                                         )
        return ResponseModel(message="False State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data=await get_non_active_property(state=state.lower())
                             ).response()
    else:
        return ResponseModel(message="All Property",
                             code=status.HTTP_200_OK,
                             success=True,
                             data=await get_all_property()
                             ).response()


@list_property.get("/property/{id}")
async def property_by_id(id: int):
    property_information = await find_particular_property_information(id)
    if property_information is None:
        raise CustomExceptionHandler(message="No Property Found",
                                     success=False,
                                     target="",
                                     code=status.HTTP_400_BAD_REQUEST
                                     )

    property_information = dict(property_information)
    info = {"facility": await get_facility_of_property(property_id=id),
            "amenity": await get_amenity_of_property(property_id=id)
            }
    property_information.update(info)
    return ResponseModel(message="Success",
                         data=property_information,
                         success=True,
                         code=status.HTTP_200_OK
                         ).response()


@list_property.patch("/property/{id}/status")
async def update_status(id: str):
    pass


@list_property.patch("/property")
async def update_property(current_user=Depends(get_current_user)):
    pass
