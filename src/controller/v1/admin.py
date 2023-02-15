from fastapi import APIRouter, Query, Path, Depends
import re

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from fastapi.encoders import jsonable_encoder
from src.constants.field import DOCTOR_REGISTRATION, DOCTOR_LOGIN
from src.constants.utilities import PHONE_REGEX, JWT_EXPIRATION_TIME
from src.models.admin_model import Admin
from src.utils.checks.admin_related_check import CheckAdminExistence
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers import jwt_utils
from src.utils.helpers.db_helpers import add_admin,admin_registered_with_mail_or_phone
from src.utils.helpers.misc import random_with_N_digits, hash_password, verify_password
from src.utils.logger.logger import logger
from src.models.admin_model import Role
from src.utils.response.data_response import ResponseModel

admin = APIRouter()


@admin.post("/register/{id}", tags=["ADMIN/GENERAL"], description="Create Call For Adding Admin's and Users")
async def register_admin(admin: Admin):
    # check if id has the authorised role which is super admin, and createdby equals to user
    admin_map = jsonable_encoder(admin)
    find_admin = CheckAdminExistence(target=DOCTOR_REGISTRATION, phone_number=admin_map["phone_number"],
                                     id=id,
                                     email=admin_map["email"])
    # check_for_role = find_admin.find_admin_by_id()
    logger.info("====== REGISTRATION PROCESS STARTED FOR {}".format(admin_map["first_name"]))
    await find_admin.find_admin_by_email()
    await find_admin.find_admin_by_phone()
    # Creating user random password, can change later
    password = str(random_with_N_digits(n=10))
    logger.info("==== RANDOMLY GENERATED PASSWORD =====")
    admin_map["password"] = hash_password(password)
    # check if who is adding is super_admin or not
    success = await add_admin(admin_map)
    if not success:
        raise CustomExceptionHandler(message="Something went wrong,Please try again later",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     target=DOCTOR_REGISTRATION,
                                     success=False
                                     )
    access_token_expires = jwt_utils.timedelta(minutes=JWT_EXPIRATION_TIME)
    access_token = await jwt_utils.create_access_token(
        data=admin_map,
        expire_delta=access_token_expires
    )
    return ResponseModel(message="Welcome to roomshala",
                         code=status.HTTP_201_CREATED,
                         success=True,
                         data={"access_token": access_token,
                               "token_type": "bearer",
                               "id": success,
                               "first_name": admin_map["first_name"],
                               "last_name": admin_map["last_name"],
                               "gender": admin_map["gender"],
                               "email": admin_map["email"],
                               "phone_number": admin_map["phone_number"],
                               "role": admin_map["role"]
                               }
                         ).response()


@admin.get("/check-registration/{email}", tags=["ADMIN/GENERAL"])
async def check_admin_registration(email: str = Path(...)):
    logger.info("===== CHECKING WHETHER THE ADMIN IS ALREADY REGISTERED OR NOT ======")
    pass


@admin.post("/login", tags=["DOCTORS/GENERAL"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("====== LOGIN VIA MAIL ========")
    success = await admin_registered_with_mail_or_phone(credential=form_data.username)
    if success is None:
        raise CustomExceptionHandler(message="Please Register Yourself",
                                     code=status.HTTP_404_NOT_FOUND,
                                     target="DOCTORS/LOGIN",
                                     success=False
                                     )

    verify_pass = verify_password(plain_password=form_data.password, hashed_passwrd=success["password"])
    if not verify_pass:
        raise CustomExceptionHandler(message="Please Check your password",
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="ADMIN_LOGIN",
                                     success=False
                                     )
    access_token_expires = jwt_utils.timedelta(minutes=JWT_EXPIRATION_TIME)
    access_token = await jwt_utils.create_access_token(
        data=success,
        expire_delta=access_token_expires
    )
    return ResponseModel(message="Successfully Login",
                         code=status.HTTP_201_CREATED,
                         success=True,
                         data={"access_token": access_token,
                               "token_type": "bearer",
                               "id": success,
                               "first_name": success["first_name"],
                               "last_name": success["last_name"],
                               "gender": success["gender"],
                               "email": success["email"],
                               "phone_number": success["phone_number"],
                               "role": success["role"]
                               }
                         ).response()