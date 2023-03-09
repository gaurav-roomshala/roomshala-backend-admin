from datetime import datetime
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.constants.field import V1_PREFIX, V1_PREFIX_PROPERTY
from src.controller.v1.amenty import amenities
from src.utils.connections.check_database_connection import DatabaseConfiguration
from src.utils.connections.db_object import db
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.tables.admin_db_tables import creating_admin_table, creating_amenties_tables, creating_facility_tables, \
    creating_codes_table, creating_blacklist_table, creating_property_table
from src.controller.v1.admin import admin
from src.controller.v1.facility import facility
from src.controller.v1.property import list_property
from starlette import status

origins = ["*"]
conn = DatabaseConfiguration()


def connections():
    conn.checking_database_connection()
    creating_admin_table()
    creating_amenties_tables()
    creating_facility_tables()
    creating_codes_table()
    creating_blacklist_table()
    creating_property_table()


connections()

app = FastAPI(title="Roomshala Backend API'S",
              version="1.0.0"
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin, prefix=V1_PREFIX)
app.include_router(facility, prefix=V1_PREFIX_PROPERTY)
app.include_router(amenities, prefix=V1_PREFIX_PROPERTY)
app.include_router(list_property, prefix=V1_PREFIX_PROPERTY)


@app.get("/health")
async def check():
    return {"status": "Ok"}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.exception_handler(CustomExceptionHandler)
async def NotFoundException(request: Request, exception: CustomExceptionHandler):
    """:return custom exceptions """
    return JSONResponse(status_code=exception.code,
                        content={"error": {"message": exception.message,
                                           "code": exception.code,
                                           "target": exception.target,
                                           "success": exception.success
                                           }
                                 }
                        )


@app.exception_handler(Exception)
async def NotHandleException(request: Request, exception: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"error": {"message": "Something Went Wrong Broken Pipeline",
                                           "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                           "target": request.url.components.path.upper(),
                                           "error": exception.__str__(),
                                           "success": False
                                           }
                                 }
                        )


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    # modify response adding custom headers
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8001)
