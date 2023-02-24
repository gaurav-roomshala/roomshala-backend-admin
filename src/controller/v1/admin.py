import uuid
from typing import Optional

from fastapi import APIRouter, Query, Path, Depends
import re

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from fastapi.encoders import jsonable_encoder
from src.constants.utilities import PHONE_REGEX, JWT_EXPIRATION_TIME
from src.models.admin_model import Admin, ForgotPassword, ResetPassword, ChangePassword, ChangeStatus
from src.utils.checks.admin_related_check import CheckAdminExistence
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers import jwt_utils
from src.utils.helpers.db_helpers import add_admin, admin_registered_with_mail_or_phone, find_exist_admin, \
    create_reset_code, check_reset_password_token, reset_admin_password, disable_reset_code, save_black_list_token, \
    get_protected_password, admin_change_password, find_exist_admin_by_id, admin_change_status, find_active_admin, \
    find_all_admin
from src.utils.helpers.jwt_utils import get_current_user, get_token_user
from src.utils.helpers.misc import random_with_N_digits, hash_password, verify_password
from src.utils.logger.logger import logger
from src.models.admin_model import Role
from src.utils.response.data_response import ResponseModel

admin = APIRouter()


@admin.post("/register/{id}", tags=["ADMIN/GENERAL"], description="Create Call For Adding Admin's and Users")
async def register_admin(admin: Admin):
    # check if id has the authorised role which is super admin, and createdby equals to user
    admin_map = jsonable_encoder(admin)
    find_admin = CheckAdminExistence(target="CHECK_ADMIN", phone_number=admin_map["phone_number"],
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
    # todo :check if who is adding is super_admin or not
    success = await add_admin(admin_map)
    if not success:
        raise CustomExceptionHandler(message="Something went wrong,Please try again later",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     target="CHECK_ADMIN",
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


@admin.post("/login", tags=["ADMIN/GENERAL"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info("====== LOGIN VIA MAIL ========")
    success = await admin_registered_with_mail_or_phone(credential=form_data.username)
    if success is None:
        raise CustomExceptionHandler(message="OOPS! No Admin Found, Register Yourself",
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
    info = jsonable_encoder(success)
    access_token = await jwt_utils.create_access_token(
        data=info,
        expire_delta=access_token_expires
    )
    return {"message": "Successfully Login",
            "code": status.HTTP_201_CREATED,
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "data": {"id": success["id"],
                     "first_name": success["first_name"],
                     "last_name": success["last_name"],
                     "gender": success["gender"],
                     "email": success["email"],
                     "phone_number": success["phone_number"],
                     "role": success["role"]}

            }


@admin.post("/forgot-password", tags=["ADMIN/GENERAL"])
async def forgot_password(request: ForgotPassword):
    response = await find_exist_admin(email=request.mail)
    if response is None:
        raise CustomExceptionHandler(message="Admin Not Found",
                                     success=False,
                                     code=status.HTTP_400_BAD_REQUEST,
                                     target="FORGOT-PASSWORD")
    reset_code = str(uuid.uuid1())
    try:
        await create_reset_code(mail=request.mail, reset_code=reset_code)
    except Exception as Why:
        logger.error("=== ERROR OCCURED IN RESETTING PASSWORD {} =====".format(Why))
        raise CustomExceptionHandler(message="Something went wrong at our end,Please try again later",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="[RESET_PASSWORD]"
                                     )
    return ResponseModel(message="Email has been sent with instructions to reset password",
                         success=True,
                         code=status.HTTP_201_CREATED,
                         data={"code": reset_code}
                         )


@admin.post("/reset-password", tags=["ADMIN/GENERAL"])
async def reset_password(request: ResetPassword):
    check_token = await check_reset_password_token(request.reset_password_token)
    if not check_token:
        logger.error("======== RESET TOKEN HAS EXPIRED =========")
        raise CustomExceptionHandler(message="Reset password token has expired,please request a new one",
                                     success=False,
                                     code=status.HTTP_404_NOT_FOUND,
                                     target="[RESET_PASSWORD]"
                                     )
    if request.new_password != request.confirm_password:
        raise CustomExceptionHandler(message="Sorry, password didn't match",
                                     success=False,
                                     code=status.HTTP_409_CONFLICT,
                                     target="RESET-PASSWORD")
    new_hashed_password = hash_password(request.new_password)
    try:
        await reset_admin_password(new_hashed_password=new_hashed_password,
                                   mail=check_token["mail"]
                                   )
        await disable_reset_code(request.reset_password_token, check_token["mail"])
    except Exception as Why:
        logger.error("===== EXCEPTION OCCURRED IN RESETTING PASSWORD ========".format(Why))
        raise CustomExceptionHandler(message="Something went wrong at our end,Please try again later",
                                     code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     success=False,
                                     target="[RESET_PASSWORD]"
                                     )
    return ResponseModel(message="Password has been reset successfully.",
                         success=True,
                         code=status.HTTP_200_OK,
                         data={}
                         ).response()


@admin.post("/profile", tags=["ADMIN/RESTRICTED"])
async def fetch_admin_info(current_user=Depends(get_current_user)):
    logger.info("======== FETCHING INFORMATION ================")
    return ResponseModel(message="Success",
                         success=True,
                         code=status.HTTP_200_OK,
                         data=current_user
                         )


@admin.get("/admin", tags=["ADMIN/GENERAL"])
async def fetch_admin(is_active: Optional[bool] = "all"):
    logger.info("======== FETCHING ADMIN AND SUPER ADMIN WITH STATE ==========".format(is_active))
    if is_active:
        success = await find_active_admin(is_active=True)
    elif not is_active:
        success = await find_active_admin(is_active=False)
    else:
        success = await find_all_admin()
    return ResponseModel(message="Please Find List",
                         data=success,
                         code=status.HTTP_200_OK,
                         success=True

                         )


@admin.patch("/status/{id}", tags=["ADMIN/RESTRICTED"])
async def update_status(id: str, state: ChangeStatus, current_user=Depends(get_current_user)):
    "super-admin can mark status to false to anyone but a admin can't mark status false of super admin"
    logger.info("====== UPDATING STATUS ==========")
    info = await find_exist_admin_by_id(id=id)
    if not info:
        raise CustomExceptionHandler(message="No admin Found",
                                     target="UPDATE_STATUS_ADMIN",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False
                                     )
    if info["role"] == "SUPER_ADMIN" and current_user["role"] == "ADMIN":
        raise CustomExceptionHandler(message="Admin Cannot Mark Status For Super Admin",
                                     target="UPDATE_STATUS_ADMIN",
                                     code=status.HTTP_404_NOT_FOUND,
                                     success=False
                                     )
    try:
        await admin_change_status(id=id, status=state.is_active)
    except Exception as Why:
        logger.error("ERROR OCCURRED IN CHANGING STATUS BECAUSE OF {}".format(Why))
        raise CustomExceptionHandler(message="Something is wrong with our server,we are working on it.",
                                     code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                     success=False,
                                     target="CHANGE_PASSWORD_DB_UPDATE"
                                     )
    else:
        return ResponseModel(message="State Update Successfully",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={"state": state.is_active}
                             ).response()


@admin.patch("/change-password", tags=["ADMIN/RESTRICTED"])
async def change_password(change_password_object: ChangePassword, current_user=Depends(get_current_user)):
    logger.info("======= CHANGING PASSWORD FOR USER {} ==========".format(current_user["first_name"]))
    cred = await get_protected_password(email=current_user["email"])
    valid_cred = verify_password(change_password_object.current_password, cred)
    if not valid_cred:
        logger.error("OOPS!! Current password does not match")
        raise CustomExceptionHandler(message="OOPS!! Your password is incorrect",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False,
                                     target="VERIFY-CURRENT_PASSWORD")
    if change_password_object.new_password != change_password_object.confirm_password:
        raise CustomExceptionHandler(message="OOPS!! New password and Confirm password does not match",
                                     code=status.HTTP_409_CONFLICT,
                                     success=False,
                                     target="VERIFY-CURRENT_PASSWORD")
    change_password_object.new_password = hash_password(change_password_object.new_password)
    try:
        await admin_change_password(change_password_object, email=current_user["email"])
    except Exception as Why:
        logger.error("ERROR OCCURRED IN CHANGING PASSWORD BECAUSE OF {}".format(Why))
        raise CustomExceptionHandler(message="Something is wrong with our server,we are working on it.",
                                     code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                     success=False,
                                     target="CHANGE_PASSWORD_DB_UPDATE"
                                     )
    else:
        return ResponseModel(message="Password has been updated successfully",
                             code=status.HTTP_200_OK,
                             success=True,
                             data={}
                             ).response()


@admin.get("/logout", tags=['ADMIN/RESTRICTED'])
async def logout(token: str = Depends(get_token_user), current_user=Depends(get_current_user)):
    # Save token of user to table blacklist
    print(current_user)
    await save_black_list_token(token, current_user["email"])
    return {
        "message": "Log out successfully",
        "code": status.HTTP_200_OK,
        "success": True,
        "target": "DOCTOR-LOGOUT"
    }
