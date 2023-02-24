from src.models.admin_model import ChangePassword
from src.utils.connections.db_object import db
from src.utils.helpers.raw_queries import QUERY_FOR_INSERTING_ADMIN
from src.utils.logger.logger import logger
from datetime import datetime
from pytz import timezone


def find_exist_admin(email: str):
    query = "select * from admin where email=:email"
    try:
        return db.fetch_one(query=query, values={"email": email})
    except Exception as Why:
        raise Exception("Something Went Wrong {}".format(Why))


def find_active_admin(is_active):
    query = "select id, first_name,last_name,phone_number,email,is_active from admin where is_active=:is_active"
    try:
        return db.fetch_all(query=query, values={"is_active": is_active})
    except Exception as Why:
        raise Exception("Something Went Wrong {}".format(Why))


def find_all_admin():
    query = "select id, first_name,last_name,phone_number,email, is_active from admin"
    try:
        return db.fetch_all(query=query)
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


def find_black_list_token(token: str):
    query = "SELECT * FROM admin_blacklists WHERE token=:token"
    try:
        return db.fetch_one(query, values={"token": token})
    except Exception as e:
        logger.error("####### EXCEPTION IN FIND_BLACK_LIST_TOKEN FUNCTION IS = {}".format(e))
    finally:
        logger.info("#### find_black_list_token FUNCTION COMPLETED ####")


def save_black_list_token(token: str, email):
    query = "INSERT INTO admin_blacklists VALUES (:token,:email)"
    return db.execute(query, values={"token": token, "email": email})


def get_protected_password(email: str):
    query = "SELECT password FROM admin WHERE email=:email"
    return db.execute(query=query, values={"email": email})


def admin_change_password(change_password_object: ChangePassword, email: str):
    query = "UPDATE admin SET password=:password,updated_on=:updated_on WHERE email=:email"
    logger.info("####### CHANGING USER PASSWORD ##########")
    try:
        return db.execute(query, values={"password": change_password_object.new_password, "email": email,
                                         "updated_on": datetime.now()})
    except Exception as e:
        logger.error("##### EXCEPTION IN CHANGING PASSWORD OF USER IS {}".format(e))


def admin_change_status(id, status):
    query = "UPDATE admin SET is_active=:is_active,updated_on=:updated_on WHERE id=:id"
    try:
        return db.execute(query=query, values={"is_active": status,
                                               "updated_on": datetime.now(),
                                               "id": id
                                               })
    except Exception as e:
        logger.error("==== EXCEPTION IN CHANGING PASSWORD =====")
