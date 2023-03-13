import sqlalchemy
from sqlalchemy import DateTime, Integer, Sequence, ARRAY

from src.constants.utilities import DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_URL, DB_USER
from src.utils.logger.logger import logger
import psycopg2


def creating_admin_table():
    logger.info("========= CREATING ADMIN TABLE ==========")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('admin',))
        if bool(cur.rowcount):
            logger.info("====== TABLE ALREADY EXIST IN THE DATABASE PASSING IT ======")
            conn.close()
            return True
        else:
            logger.warning("======= ADMIN TABLE DOESN'T EXIST, CREATING IT ========")
            metadata = sqlalchemy.MetaData()
            admin = sqlalchemy.Table(
                "admin",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("admin_id_seq"), primary_key=True),
                sqlalchemy.Column("first_name", sqlalchemy.String()),
                sqlalchemy.Column("last_name", sqlalchemy.String()),
                sqlalchemy.Column("gender", sqlalchemy.String()),
                sqlalchemy.Column("email", sqlalchemy.String()),
                sqlalchemy.Column("password", sqlalchemy.String()),
                sqlalchemy.Column("phone_number", sqlalchemy.String()),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean()),
                sqlalchemy.Column("role", sqlalchemy.String),
                sqlalchemy.Column("created_on", DateTime),
                sqlalchemy.Column("created_by", sqlalchemy.String()),
                sqlalchemy.Column("updated_on", DateTime),
                sqlalchemy.Column("updated_by", sqlalchemy.String()),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return admin
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING ADMIN TABLE {} ########".format(e))
        raise Exception("SOMETHING WENT WRONG IN CREATING ADMIN TABLE")


def creating_codes_table():
    try:
        logger.info(" ########## GOING FOR CODES TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('admin_code',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            logger.info("#### CODES TABLE DOESN'T EXIST #### ")
            metadata = sqlalchemy.MetaData()
            codes = sqlalchemy.Table(
                "admin_code",
                metadata,
                sqlalchemy.Column("id", Integer, Sequence("admin_code_id_seq"), primary_key=True),
                sqlalchemy.Column("mail", sqlalchemy.String(100)),
                sqlalchemy.Column("reset_code", sqlalchemy.String(60)),
                sqlalchemy.Column("expired_in", DateTime),
                sqlalchemy.Column("status", sqlalchemy.String(1))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return codes
    except Exception as e:
        logger.error("{}".format(e))


def creating_blacklist_table():
    try:
        logger.info(" ########## GOING FOR BLACKLIST TABLES ##############")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('admin_blacklists',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            blacklists = sqlalchemy.Table(
                "admin_blacklists", metadata,
                sqlalchemy.Column("token", sqlalchemy.String(700), unique=True),
                sqlalchemy.Column("email", sqlalchemy.String(100))
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3, max_overflow=0)
            metadata.create_all(engine)
            conn.close()
            return blacklists
    except Exception as e:
        logger.error("{}".format(e))


def creating_facility_tables():
    try:
        logger.info("======= GOING FOR FACILITY TABLE ==============")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('facilities',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            specialisations = sqlalchemy.Table(
                "facilities", metadata,
                sqlalchemy.Column("id", Integer, Sequence("facilities_id_seq"), primary_key=True),
                sqlalchemy.Column("name", sqlalchemy.String(100)),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return specialisations
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING FACILITIES TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE FACILITIES TABLE FUNCTION OVER ###### ")


def creating_amenties_tables():
    try:
        logger.info("======= GOING FOR AMENTIES TABLE ==============")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('amenties',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            specialisations = sqlalchemy.Table(
                "amenties", metadata,
                sqlalchemy.Column("id", Integer, Sequence("amenties_id_seq"), primary_key=True),
                sqlalchemy.Column("name", sqlalchemy.String(100)),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("created_on", DateTime),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return specialisations
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING AMENTIES TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE AMENTIES TABLE FUNCTION OVER ###### ")


def creating_property_table():
    try:
        logger.info("======= GOING FOR PROPERTY TABLE ==============")
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('properties',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            properties = sqlalchemy.Table(
                "properties", metadata,
                sqlalchemy.Column("id", Integer, Sequence("properties_id_seq"), primary_key=True),
                sqlalchemy.Column("property_code", sqlalchemy.String(100)),
                sqlalchemy.Column("property_name", sqlalchemy.String(100)),
                sqlalchemy.Column("property_type", sqlalchemy.String(100)),
                sqlalchemy.Column("floor_numbers", sqlalchemy.Integer),
                sqlalchemy.Column("property_description", sqlalchemy.String(500)),
                sqlalchemy.Column("property_email_id", sqlalchemy.String(100)),
                sqlalchemy.Column("property_mobile_number", sqlalchemy.String(100)),
                sqlalchemy.Column("complete_address", sqlalchemy.String(500)),
                sqlalchemy.Column("locality", sqlalchemy.String(50)),
                sqlalchemy.Column("landmark", sqlalchemy.String(100)),
                sqlalchemy.Column("pincode", sqlalchemy.String(100)),
                sqlalchemy.Column("city", sqlalchemy.String(100)),
                sqlalchemy.Column("state", sqlalchemy.String(100)),
                sqlalchemy.Column("longitude", sqlalchemy.String(100)),
                sqlalchemy.Column("latitude", sqlalchemy.String(100)),
                sqlalchemy.Column("necessary_documents", sqlalchemy.JSON),
                sqlalchemy.Column("property_docs", sqlalchemy.JSON),
                sqlalchemy.Column("is_active", sqlalchemy.Boolean),
                sqlalchemy.Column("created_on", DateTime),
                sqlalchemy.Column("created_by", sqlalchemy.String(100)),
                sqlalchemy.Column("updated_on", DateTime),
                sqlalchemy.Column("updated_by", sqlalchemy.String(100)),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return properties
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING PROPERTY TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE PROPERTY TABLE FUNCTION OVER ###### ")


def property_facility_map():
    logger.info("======= GOING FOR PROPERTY_FACILITY_MAP =================")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('property_facility_map',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            property_facility_map = sqlalchemy.Table(
                "property_facility_map", metadata,
                sqlalchemy.Column("id", Integer, Sequence("property_facility_map_id_seq"), primary_key=True),
                sqlalchemy.Column("property_id", Integer),
                sqlalchemy.Column("facility_id", Integer),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return property_facility_map
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING PROPERTY_FACILITY_MAP TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE PROPERTY_FACILITY_MAP TABLE FUNCTION OVER ###### ")


def property_amenity_map():
    logger.info("======= GOING FOR property_amenity_map =================")
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD, port=DB_PORT)
        cur = conn.cursor()
        cur.execute("select * from information_schema.tables where table_name=%s", ('property_amenity_map',))
        if bool(cur.rowcount):
            logger.info("#### TABLE ALREADY EXIST IN THE DATABASE PASSING IT")
            conn.close()
            return True
        else:
            metadata = sqlalchemy.MetaData()
            property_amenity_map = sqlalchemy.Table(
                "property_amenity_map", metadata,
                sqlalchemy.Column("id", Integer, Sequence("property_amenity_map_id_seq"), primary_key=True),
                sqlalchemy.Column("property_id", Integer),
                sqlalchemy.Column("amenity_id", Integer),
            )
            engine = sqlalchemy.create_engine(
                DB_URL, pool_size=3)
            metadata.create_all(engine)
            conn.close()
            return property_amenity_map
    except Exception as e:
        logger.error("######## WENT WRONG IN CREATING property_amenity_map TABLE {} ########".format(e))
    finally:
        logger.info("###### CREATE property_amenity_map TABLE FUNCTION OVER ######")
