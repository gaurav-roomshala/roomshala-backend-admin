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
        return db.execute(QUERY_FOR_INSERTING_ADMIN,values={"first_name":admin["first_name"],
                                                            "last_name":admin["last_name"],
                                                            "gender":admin["gender"],
                                                            "email":admin["email"],
                                                            "password":admin["password"],
                                                            "phone_number":admin["phone_number"],
                                                            "is_active":admin["is_active"],
                                                            "role":admin["role"],
                                                            "created_by":admin["created_by"],
                                                            "updated_by":admin["updated_by"]
                                                            })
    except Exception as Why:
        logger.error("==== ERROR IN ADDING ADMIN DUE TO {} ===".format(Why))
        return False


def admin_registered_with_mail_or_phone(credential: str):
    query = "SELECT * FROM admin WHERE email=:email OR phone_number=:phone_number"
    return db.fetch_one(query=query, values={"email": credential, "phone_number": credential})
