from datetime import datetime
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.constants.field import V1_PREFIX
from src.utils.connections.check_database_connection import DatabaseConfiguration
from src.utils.connections.db_object import db
from src.utils.custom_exceptions.custom_exceptions import CustomExceptionHandler
from src.utils.tables.admin_db_tables import creating_admin_table

origins = ["*"]
conn = DatabaseConfiguration()


def connections():
    conn.checking_database_connection()
    creating_admin_table()

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
