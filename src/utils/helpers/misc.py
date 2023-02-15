from random import randint
from passlib.context import CryptContext
from src.constants.field import BCRYPT_SCHEMA
pwd_context = CryptContext(schemes=[BCRYPT_SCHEMA])

def random_with_N_digits(n):
    return "Hello@123"
    # range_start = 10 ** (n - 1)
    # range_end = (10 ** n) - 1
    # return randint(range_start, range_end)



def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_passwrd: str):
    return pwd_context.verify(plain_password, hashed_passwrd)