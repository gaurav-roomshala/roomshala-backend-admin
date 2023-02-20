from src.utils.connections.db_object import db
from src.utils.helpers.raw_queries import QUERY_FOR_INSERTING_ADMIN
from src.utils.logger.logger import logger
from datetime import datetime, timezone


def find_exist_admin(email: str):
    query = "select * from admin where email=:email"
    try:
        return db.fetch_one(query=query, values={"email": email})
    except Exception as Why:
        raise Exception("Something Went Wrong {}".format(Why))


def find_exist_admin_by_id(id):
    query = "select * from admin where id=:id"
    try:
        return db.fetch_one(query=query, values={"id": id})
    except Exception as Why:
        raise Exception("Something Went Wrong {}".format(Why))


def find_exist_admin_via_phone(phone_number: str):
    query = "select * from admin where phone_number=:phone_number"
    try:
        return db.fetch_one(query=query, values={"phone_number": phone_number})
    except Exception as Why:
        raise Exception("Something Went Wrong {}".format(Why))


def add_admin(admin):
    try:
        logger.info("===== CREATING ADMIN ENTRY ============")
        return db.execute(QUERY_FOR_INSERTING_ADMIN, values={"first_name": admin["first_name"],
                                                             "last_name": admin["last_name"],
                                                             "gender": admin["gender"],
                                                             "email": admin["email"],
                                                             "password": admin["password"],
                                                             "phone_number": admin["phone_number"],
                                                             "is_active": admin["is_active"],
                                                             "role": admin["role"],
                                                             "created_by": admin["created_by"],
                                                             "updated_by": admin["updated_by"]
                                                             })
    except Exception as Why:
        logger.error("==== ERROR IN ADDING ADMIN DUE TO {} ===".format(Why))
        return False


def admin_registered_with_mail_or_phone(credential: str):
    query = "SELECT * FROM admin WHERE email=:email OR phone_number=:phone_number"
    return db.fetch_one(query=query, values={"email": credential, "phone_number": credential})


def create_reset_code(mail: str, reset_code: str):
    try:
        query = """INSERT INTO admin_code VALUES (nextval('admin_code_id_seq'),:mail,:reset_code,now() at time zone 'UTC',
        '1') """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query, values={"mail": mail, "reset_code": reset_code})
    except Exception as e:
        logger.error("##### EXCEPTION IN create_reset_code FUNCTION IS {}".format(e))
    finally:
        logger.info("#### create_reset_code FUNCTION COMPLETED ####")


def check_reset_password_token(reset_password_token: str):
    try:
        query = """SELECT * FROM admin_code WHERE status='1' AND reset_code=:reset_password_token AND expired_in >= now() AT TIME 
        ZONE 'UTC' - INTERVAL '10 minutes' """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.fetch_one(query, values={"reset_password_token": reset_password_token})
    except Exception as e:
        logger.error("##### EXCEPTION IN check_reset_password_token FUNCTION IS {}".format(e))
    finally:
        logger.info("#### check_reset_password_token FUNCTION COMPLETED ####")


def reset_admin_password(new_hashed_password: str, mail: str):
    try:
        query = """ UPDATE admin SET password=:password WHERE email=:email """
        logger.info("#### PROCEEDING FURTHER FOR THE EXECUTION OF QUERY")
        return db.execute(query, values={"password": new_hashed_password, "email": mail})
    except Exception as e:
        logger.error("##### EXCEPTION IN reset_password_user FUNCTION IS {}".format(e))
    finally:
        logger.info("#### reset_password_user FUNCTION COMPLETED ####")


def disable_reset_code(reset_password_token: str, mail: str):
    query = "UPDATE admin_code SET status='9' WHERE status='1' AND reset_code=:reset_code AND mail=:mail"
    try:
        return db.execute(query, values={"reset_code": reset_password_token, "mail": mail})
    except Exception as e:
        logger.error("#### EXCEPTION IN DISABLE_RESET_CODE IS {}".format(e))
    finally:
        logger.info("#### disable_reset_password_user FUNCTION COMPLETED ####")
