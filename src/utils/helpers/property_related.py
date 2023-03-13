from src.utils.connections.db_object import db
from src.utils.logger.logger import logger

QUERY_FOR_LISTING_PROPERTY = """INSERT INTO properties VALUES (nextval('properties_id_seq'),:property_code,:property_name,:property_type,:floor_numbers,
 :property_description,:property_email_id,:property_mobile_number,:complete_address,:locality,:landmark,:pincode,:city,:state,:longitude,
 :latitude,:necessary_documents,:property_docs,:is_active,now() at time zone 'UTC',:created_by,now() at time zone 'UTC',:updated_by) RETURNING id """

QUERY_FOR_PROPERTY_FACILITY_MAP = "INSERT INTO property_facility_map VALUES (nextval('property_facility_map_id_seq'),:property_id,:facility_id) "

QUERY_FOR_PROPERTY_AMENITY_MAP = "INSERT INTO property_amenity_map VALUES (nextval('property_amenity_map_id_seq')," \
                                 ":property_id,:amenity_id) "


def property_last_entry():
    logger.info("======= FINDING LAST PROPERTY ========= ")
    query = "SELECT LAST(id) as id FROM properties"
    try:
        return db.fetch_one(query=query)
    except Exception as Why:
        logger.error("##### EXCEPTION IN FINDING_LAST_PROPERTY_ENTRY FUNCTION IS {}".format(Why))
    finally:
        logger.info("#### FIND FINDING_LAST_PROPERTY_ENTRY FUNCTION COMPLETED ####")


def find_property_email_id(property_email_id):
    try:
        logger.info("=========== FINDING EMAIL ===============================")
        query = "SELECT * FROM properties WHERE property_email_id=:property_email_id"
        return db.fetch_one(query=query, values={"property_email_id": property_email_id})
    except Exception as e:
        logger.error("##### EXCEPTION IN FINDING_PARTICULAR_EMAIL_ID FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND FINDING_PARTICULAR_EMAIL_ID FUNCTION COMPLETED ####")


def find_property_mobile_number(property_mobile_number):
    try:
        logger.info("======== FINDING PHONE =====")
        query = "SELECT * FROM properties WHERE property_mobile_number=:property_mobile_number"
        return db.fetch_one(query=query, values={"property_mobile_number": property_mobile_number})
    except Exception as e:
        logger.error("##### EXCEPTION IN FINDING_PARTICULAR_EMAIL_ID FUNCTION IS {}".format(e))
    finally:
        logger.info("#### FIND FINDING_PARTICULAR_EMAIL_ID FUNCTION COMPLETED ####")


def find_particular_property_information(id: int):
    query = "SELECT * FROM properties WHERE id=:id"
    return db.fetch_one(query=query, values={"id": id})


async def list_new_property(property, code):
    async with db.transaction():
        print(property)
        transaction = await db.transaction()
        try:
            logger.info("======= LISTING PROPERTY, TRANSACTION IN PROCESS ========")
            property_id = await db.execute(query=QUERY_FOR_LISTING_PROPERTY, values={"property_code": code,
                                                                                     "property_name": property.property_name,
                                                                                     "property_type": property.property_type,
                                                                                     "floor_numbers": property.floor_numbers,
                                                                                     "property_description": property.property_description,
                                                                                     "property_email_id": property.property_email_id,
                                                                                     "property_mobile_number": property.property_mobile_number,
                                                                                     "complete_address": property.complete_address,
                                                                                     "locality": property.locality,
                                                                                     "landmark": property.landmark,
                                                                                     "pincode": property.pincode,
                                                                                     "city": property.city,
                                                                                     "state": property.state,
                                                                                     "longitude": property.longitude,
                                                                                     "latitude": property.latitude,
                                                                                     "necessary_documents": property.necessary_documents,
                                                                                     "property_docs": property.property_docs,
                                                                                     "is_active": False,
                                                                                     "created_by": property.created_by,
                                                                                     "updated_by": property.updated_by
                                                                                     })
            logger.info("####### SUCCESS IN PROPERTY TABLE #########")
            await db.execute(query="UPDATE properties SET property_code=:property_code WHERE id=:id",values={"property_code":"RS-"+str(property_id),"id":property_id})
            map_object = []
            for get_index in property.facilities:
                object_map = {"property_id": property_id,
                              "facility_id": get_index
                              }

                map_object.append(object_map)
            logger.info("####### GOING FOR EXECUTION OF PROPERTY FACILITY MAP ########### ")
            await db.execute_many(query=QUERY_FOR_PROPERTY_FACILITY_MAP, values=map_object)
            logger.info("####### SUCCESSFULLY EXECUTED PROPERTY FACILITY MAP ########### ")
            map_object = []
            for get_index in property.amenities:
                object_map = {"property_id": property_id,
                              "amenity_id": get_index
                              }

                map_object.append(object_map)
            await db.execute_many(query=QUERY_FOR_PROPERTY_AMENITY_MAP, values=map_object)
            logger.info("====== SUCCESS =========")
        except Exception as Why:
            logger.error("######### ERROR IN THE QUERY BECAUSE {} ".format(Why))
            logger.info("########## ROLLING BACK TRANSACTIONS #################")
            await transaction.rollback()
            return False, ""
        else:
            logger.info("##### ALL WENT WELL COMMITTING TRANSACTION ########")
            await transaction.commit()
            logger.info("###### TRANSACTION COMMITTED AND SUCCESS TRUE #######")
            return True, property_id


def get_active_property(state):
    try:
        query = "select * from properties where is_active=:is_active and state=:state order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET PROPERTIES")
        return db.fetch_all(query, values={"is_active": True, "state": state})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_AMENITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_AMENITIES FUNCTION COMPLETED ####")


def get_non_active_property(state):
    try:
        print(state)
        query = "select * from properties where is_active=:is_active and state=:state order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET PROPERTIES")
        return db.fetch_all(query, values={"is_active": False, "state": state})
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_AMENITIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_AMENITIES FUNCTION COMPLETED ####")


def get_all_property():
    try:
        query = "select * from properties order by created_on desc"
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY OF GET PROPERTIES")
        return db.fetch_all(query)
    except Exception as e:
        logger.error("##### EXCEPTION IN GET_ALL_PROPERTIES FUNCTION IS {}".format(e))
    finally:
        logger.info("#### GET_ALL_PROPERTIES FUNCTION COMPLETED ####")
