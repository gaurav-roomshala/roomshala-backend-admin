import sqlalchemy
from sqlalchemy import DateTime, Integer, Sequence, ARRAY

from src.constants.utilities import DB_NAME, DB_HOST, DB_PASSWORD,DB_PORT,DB_URL,DB_USER
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
                sqlalchemy.Column("first name", sqlalchemy.String()),
                sqlalchemy.Column("last name", sqlalchemy.String()),
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





