from src.models.amenties import Amenties
from src.utils.connections.db_object import db
from src.utils.helpers.raw_queries import QUERY_FOR_SAVING_AMENITIES
from src.utils.logger.logger import logger


def find_particular_amenity_by_id(id):
    try:
        logger.info("=== FINDING AMENITY =====")
        query = "SELECT * FROM amenties WHERE id=:id"
        return db.fetch_one(query=query, values={"id": id})
    except Exception as e:
        logger.error("##### EXCEPTION IN FINDING_PARTICULAR_ID FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_AMENITY FUNCTION COMPLETED ####")


def find_particular_amenity(name):
    try:
        logger.info("===== ADDING AMENITY =======")
        query = "SELECT * FROM amenties WHERE name=:name"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FINDING PARTICULAR ####")
        return db.fetch_one(query=query, values={"name": name})
    except Exception as e:
        logger.error("##### EXCEPTION IN AMENITY FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_AMENITY FUNCTION COMPLETED ####")


def save_amenity(amen: Amenties):
    try:
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FACILITY")
        return db.execute(QUERY_FOR_SAVING_AMENITIES, values={"name": amen.name,
                                                              "is_active": True
                                                              })
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_AMENITIES FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_AMENITIES FUNCTION COMPLETED ####")


def get_true_amenity():
    try:
        query = "select * from amenties where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET AMENITIES")
        return db.fetch_all(query, values={"is_active": True})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_AMENITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_AMENITIES FUNCTION COMPLETED ####")


def get_false_amenity():
    try:
        query = "select * from amenties where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET FACILITIES")
        return db.fetch_all(query, values={"is_active": False})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_AMENITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_AMENITIES FUNCTION COMPLETED ####")


def get_all_amenity():
    try:
        query = "select * from amenties order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET FACILITIES")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_AMENITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_AMENITIES FUNCTION COMPLETED ####")


def update_amenity_state(id, is_active):
    query = "UPDATE amenties SET is_active=:is_active WHERE id=:id RETURNING id"
    try:
        return db.execute(query, values={"is_active": is_active, "id": id})
    except Exception as e:
        logger.error("### ERROR IN UPDATING AMENITIES {} #####".format(e))
    finally:
        logger.info("##### UPDATE AMENITIES METHOD OVER ####")


async def check_if_amenity_valid(amenity):
    if len(amenity) == 0:
        return False
    available_amenity_arr = []
    true_amenity = await get_true_amenity()
    for i in true_amenity:
        check = dict(i)
        available_amenity_arr.append(check["id"])
    for verify in amenity:
        if verify not in available_amenity_arr:
            return False
        else:
            continue
    return True


QUERY_FOR_FINDING_PROPERTY_AMENITY = "SELECT property_amenity_map.property_id, amenties.name,amenties.id," \
                                      "amenties.is_active FROM property_amenity_map INNER JOIN amenties ON " \
                                      "property_amenity_map.amenity_id=amenties.id WHERE property_id=:property_id "

def get_amenity_of_property(property_id:int):
    return db.fetch_all(query=QUERY_FOR_FINDING_PROPERTY_AMENITY,values={"property_id":property_id})
