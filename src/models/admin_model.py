from pydantic import BaseModel, Field, validator
from enum import Enum

from starlette import status

from src.constants.utilities import EMAIL_REGEX, PHONE_REGEX
from typing import Optional, Dict
from typing import List
from fastapi import Query
from datetime import datetime
import re
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler


class Gender(str, Enum):
    male = "MALE"
    female = "FEMALE"
    other = "OTHER"


class Role(str, Enum):
    super_admin = "SUPER_ADMIN"
    admin = "ADMIN"


class ChangeStatus(BaseModel):
    is_active: bool


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str


class ForgotPassword(BaseModel):
    mail: str = Field(..., description="Mail")


class SuperAdmin(BaseModel):
    first_name = "RAJAT"
    last_name = "Sharma"
    gender = "Male"
    email = "rajat@roomshala.com"
    phone_number = "9899308683"
    role = "SUPER_ADMIN"
    is_active = True
    created_by = "rajat@roomshala.com"
    updated_by = "rajat@roomshala.com"


class Admin(BaseModel):
    first_name: str = Field(..., )
    last_name: str = Field(...)
    gender: Gender
    email: str = Field(...)
    phone_number: str = Field(...)
    is_active: bool = None
    role: Role
    created_on: datetime = None
    created_by: str = Field(..., description="")
    updated_on: datetime = None
    updated_by: str = Field(..., description="")

    @validator("first_name")
    @classmethod
    def return_lower(cls, value):
        return value.lower()

    @validator("email")
    @classmethod
    def check_email(cls, value):
        pattern = re.compile(EMAIL_REGEX)
        if not pattern.match(value):
            raise CustomExceptionHandler(message="Please enter a valid email",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target="",
                                         success=False
                                         )
        return value

    @validator("phone_number")
    @classmethod
    def check_phone_number_regex(cls, value):
        pattern = re.compile(PHONE_REGEX)
        if not pattern.match(value):
            raise CustomExceptionHandler(message="Please enter a valid phone number",
                                         code=status.HTTP_400_BAD_REQUEST,
                                         target="",
                                         success=False
                                         )
        return value
