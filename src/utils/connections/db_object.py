from src.constants.utilities import DB_URL
from databases import Database

from src.utils.custom_exceptions.custom_exceptions import DatabaseConnectionError
from src.utils.logger.logger import logger
try:
    logger.info(" ########## GOING FOR CONNECTION ##############")
    db = Database("postgresql://postgres:Anubhav1234@roomshalainstancetest.clwy0rgkmro3.us-east-1.rds.amazonaws.com:5432/roomshala_admin")
except Exception as e:
    logger.error("###### EXCEPTION IN DB_OBJECT IS {} ###########".format(e))
    raise DatabaseConnectionError(message="Error Occur in Database {}".format(e))
