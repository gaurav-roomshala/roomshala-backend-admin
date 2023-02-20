from src.models.faciities import Facilities
from src.utils.connections.db_object import db
from src.utils.helpers.raw_queries import QUERY_FOR_SAVING_FACILITY
from src.utils.logger.logger import logger


def find_particular_facility_by_id(id):
    try:
        logger.info("=== FINDING FACILITY =====")
        query = "SELECT * FROM facilities WHERE id=:id"
        return db.fetch_one(query=query, values={"id": id})
    except Exception as e:
        logger.error("##### EXCEPTION IN FINDING_PARTICULAR_ID FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_FACILITY FUNCTION COMPLETED ####")


def find_particular_facility(name):
    try:
        logger.info("===== ADDING FACILITY =======")
        query = "SELECT * FROM facilities WHERE name=:name"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FINDING PARTICULAR ####")
        return db.fetch_one(query=query, values={"name": name})
    except Exception as e:
        logger.error("##### EXCEPTION IN FACILITY FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND PARTICULAR_FACILITY FUNCTION COMPLETED ####")


def save_facility(facility: Facilities):
    try:
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF FACILITY")
        return db.execute(QUERY_FOR_SAVING_FACILITY, values={"name": facility.name,
                                                             "is_active": True
                                                             })
    except Exception as e:
        logger.error("##### EXCEPTION IN SAVE_FACILITY FUNCTION IS {}".format(e))
        return False
    finally:
        logger.info("#### FIND SAVE_FACILITY FUNCTION COMPLETED ####")


def get_true_facility():
    try:
        query = "select * from facilities where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET FACILITIES")
        return db.fetch_all(query, values={"is_active": True})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_FACILITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_FACILITIES FUNCTION COMPLETED ####")


def get_false_facility():
    try:
        query = "select * from facilities where is_active=:is_active order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET FACILITIES")
        return db.fetch_all(query, values={"is_active": False})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_FACILITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_FACILITIES FUNCTION COMPLETED ####")


def get_all_facility():
    try:
        query = "select * from facilities order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET FACILITIES")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_FACILITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_FACILITIES FUNCTION COMPLETED ####")


def update_facility_state(id, is_active):
    query = "UPDATE facilities SET is_active=:is_active WHERE id=:id RETURNING id"
    try:
        return db.execute(query, values={"is_active": is_active, "id": id})
    except Exception as e:
        logger.error("### ERROR IN UPDATING FACILITIES {} #####".format(e))
    finally:
        logger.info("##### UPDATE FACILITIES METHOD OVER ####")
