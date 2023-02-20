from fastapi import Request, Path, Query
from fastapi import status, APIRouter, HTTPException, Depends
from src.models.faciities import Facilities, FACILITIES_TYPE, FacilityUpdate
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers.facility_related import find_particular_facility, save_facility, get_true_facility, \
    get_false_facility, get_all_facility, find_particular_facility_by_id, update_facility_state
from src.utils.logger.logger import logger
from src.utils.response.data_response import ResponseModel

facility = APIRouter()

TRUE = "true"
false = "false"


@facility.post("/facility", tags=["PROPERTY/SPECIFICATION"])
async def add_facility(fac: Facilities):
    check_facility = await find_particular_facility(name=fac.name)
    if check_facility is not None:
        raise CustomExceptionHandler(message="Facility Already Added",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False,
                                     target="Post Facility")
    try:
        await save_facility(fac)
        return ResponseModel(message="facility added successfully",
                             code=status.HTTP_201_CREATED,
                             success=True,
                             data={"name": fac.name}
                             ).response()
    except Exception as Why:
        logger.error("===== ERROR IN CREATING FACILITY DUE TO {} ========".format(Why))
        raise CustomExceptionHandler(message="Unable to save facility",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="CREATE_FACILITY_DUE_{}".format(Why)
                                     )


@facility.get("/facility-types", tags=["PROPERTY/SPECIFICATION"])
async def facility_types():
    return ResponseModel(message="Facility Types",
                         code=status.HTTP_200_OK,
                         success=False,
                         data={"types": FACILITIES_TYPE}
                         )


@facility.get("/facility", tags=["PROPERTY/SPECIFICATION"])
async def fetch_facility(state: str = Query(None, description="to get which state facility")):
    if state == TRUE:
        return ResponseModel(message="True State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={"name": await get_true_facility()}
                             ).response()
    if state == "false":
        return ResponseModel(message="False State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={"name": await get_false_facility()}
                             ).response()
    return ResponseModel(message="Gen State Facility",
                         code=status.HTTP_200_OK,
                         success=True,
                         data={"name": await get_all_facility()}
                         ).response()


@facility.patch("/facility/{id}",tags=["PROPERTY/SPECIFICATION"])
async def update_facility(fac:FacilityUpdate,id:int=Path(...,description="Should be passed as integer")):
    response = await find_particular_facility_by_id(id=id)
    if response is None:
        logger.error("########### NO FACILITY IS FOUND FOR GIVEN ID ############")
        raise CustomExceptionHandler(message="We regret,Something went wrong our at end.",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False,
                                     target="[FACILITY DOES NOT EXIST]")
    response = await update_facility_state(id=id,is_active=fac.is_active)
    if not response:
        raise CustomExceptionHandler(message="We regret,Something went wrong our at end.",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="[CANNOT ABLE TO UPDATE FACILITY]")
    return ResponseModel(message="Successfully update the facility",
                         code=status.HTTP_200_OK,
                         success=True,
                         data={"id":id}
                         ).response()