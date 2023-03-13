import json
from random import randint
from passlib.context import CryptContext
from src.constants.field import BCRYPT_SCHEMA

pwd_context = CryptContext(schemes=[BCRYPT_SCHEMA])


def random_with_N_digits(n):
    return "Hello@123"
    # range_start = 10 ** (n - 1)
    # range_end = (10 ** n) - 1
    # return randint(range_start, range_end)


def check_documents(necessary):
    if necessary["aadhar"] is None or necessary["aadhar"] == "" or necessary["aadhar"] == "string":
        return False
    if necessary["pancard"] is None or necessary["pancard"] == "" or necessary["pancard"] == "string":
        return False
    # modify

    return True


def modify_docs(docs):
    return json.dumps(docs)



def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_passwrd: str):
    return pwd_context.verify(plain_password, hashed_passwrd)


print(verify_password(plain_password="Anubhav@1234",
                      hashed_passwrd="$2b$12$GBYAwZwVFSVkMvraQ2VL/OLALc3HUip6tYZGeX0AaE2IFHT/EMkeK"))
