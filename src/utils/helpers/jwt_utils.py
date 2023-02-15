from datetime import datetime, timedelta

from src.constants.utilities import JWT_EXPIRATION_TIME, JWT_SECRET_KEY, JWT_ALGORITHM
import jwt


async def create_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
