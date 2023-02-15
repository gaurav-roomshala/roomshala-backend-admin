from starlette import status
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.helpers.db_helpers import find_exist_admin, find_exist_admin_via_phone, find_exist_admin_by_id


class CheckAdminExistence(object):
    def __init__(self, target: str, id=None, phone_number=None, email=None):
        self.phone_number = phone_number
        self.email = email
        self.target = target
        self.id = id

    async def find_admin_by_id(self):
        response = await find_exist_admin_by_id(id=self.id)
        if response is None:
            raise CustomExceptionHandler(message="Something went wrong,Please try again later",
                                         code=status.HTTP_404_NOT_FOUND,
                                         success=False,
                                         target=self.target
                                         )
        return response

    async def find_admin_by_email(self):
        response = await find_exist_admin(email=self.email)
        if response is not None:
            raise CustomExceptionHandler(message="Admin is already registered with given email",
                                         code=status.HTTP_409_CONFLICT,
                                         success=False,
                                         target=self.target
                                         )
        return response

    async def find_admin_by_phone(self):
        response = await find_exist_admin_via_phone(phone_number=self.phone_number)
        if response is not None:
            raise CustomExceptionHandler(message="Admin is already registered with given phone number",
                                         code=status.HTTP_409_CONFLICT,
                                         success=False,
                                         target=self.target
                                         )
        return response


