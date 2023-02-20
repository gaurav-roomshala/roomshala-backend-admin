from fastapi import Request, Path, Query
from fastapi import status, APIRouter, HTTPException, Depends
from src.models.amenties import Amenties, AmenityUpdate
from src.utils.helpers.amenty_related import find_particular_amenity, save_amenity, get_true_amenity, get_false_amenity, \
    get_all_amenity, find_particular_amenity_by_id, update_amenity_state
from src.utils.logger.logger import logger
from src.utils.response.data_response import ResponseModel
from src.constants.field import TRUE, FALSE
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler

amenities = APIRouter()


@amenities.post("/amenity", tags=["PROPERTY/SPECIFICATION"])
async def amenity(am: Amenties):
    check_amenity = await find_particular_amenity(name=am.name)
    if check_amenity is not None:
        raise CustomExceptionHandler(message="Amenity Already Added",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False,
                                     target="[Post AMENITY]")
    try:
        await save_amenity(amen=am)
    except Exception as Why:
        logger.error("===== ERROR IN CREATING AMENITY DUE TO {} ========".format(Why))
        raise CustomExceptionHandler(message="Unable to save AMENITY",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="CREATE_AMENITY_DUE_{}".format(Why)
                                     )
    return ResponseModel(message="Amenity added successfully",
                         code=status.HTTP_201_CREATED,
                         success=True,
                         data={"name": am.name}
                         ).response()


@amenities.get("/amenity", tags=["PROPERTY/SPECIFICATION"])
async def fetch_facility(state: str = Query(None, description="to get which state amenity")):
    if state == TRUE:
        return ResponseModel(message="True State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={"name": await get_true_amenity()}
                             ).response()
    if state == "false":
        return ResponseModel(message="False State Facility",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={"name": await get_false_amenity()}
                             ).response()
    return ResponseModel(message="Gen State Facility",
                         code=status.HTTP_200_OK,
                         success=True,
                         data={"name": await get_all_amenity()}
                         ).response()


@amenities.patch("/amenity/{id}", tags=["PROPERTY/SPECIFICATION"])
async def update_amenity(fac: AmenityUpdate, id: int = Path(..., description="Should be passed as integer")):
    response = await find_particular_amenity_by_id(id=id)
    if response is None:
        logger.error("########### NO AMENITY IS FOUND FOR GIVEN ID ############")
        raise CustomExceptionHandler(message="We regret,Something went wrong our at end.",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False,
                                     target="[AMENITY DOES NOT EXIST]")
    response = await update_amenity_state(id=id, is_active=fac.is_active)
    if not response:
        raise CustomExceptionHandler(message="We regret,Something went wrong our at end.",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="[CANNOT ABLE TO UPDATE AMENITY]")
    return ResponseModel(message="Successfully update the AMENITY",
                         code=status.HTTP_200_OK,
                         success=True,
                         data={"id": id}
                         ).response()
