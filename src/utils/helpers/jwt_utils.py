from datetime import datetime, timedelta
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.constants.utilities import JWT_EXPIRATION_TIME, JWT_SECRET_KEY, JWT_ALGORITHM
import jwt


async def create_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/admin/login"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        # Check blacklist token
        black_list_token = await find_black_list_token(token)
        if black_list_token:
            print("error in creds")
            raise credential_exception
        # Check if user exist or not
        result = await find_exist_username_email(check=username)
        if not result:
            raise CustomExceptionHandler(message="You are not registered yet,please register yourself",
                                         code=status.HTTP_404_NOT_FOUND,
                                         success=False,
                                         target="JWT-VERIFICATION"
                                         )
        return {"id": result["id"],
                "full_name": result["full_name"],
                "mail": result["mail"],
                "phone_number": result["phone_number"],
                "gender": result["gender"],
                "experience": result["experience"],
                "url": result["url"],
                "about": result["about"]
                }
    except ValidationError:
        raise credential_exception
    except Exception as e:
        raise CustomExceptionHandler(message="Something went wrong,please try again later",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="JWT-VERIFICATION CAUSED[{}]".format(e)
                                     )
