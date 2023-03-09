from src.utils.connections.db_object import db
from src.utils.logger.logger import logger



QUERY_FOR_LISTING_PROPERTY = """INSERT INTO properties VALUES """

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



async def list_new_property(property):
    async with db.transaction():
        transaction = await db.transaction()
        try:
            logger.info("======= LISTING PROPERTY, TRANSACTION IN PROCESS ========")
            property_id = await db.execute()

