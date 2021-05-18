from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from settings import ProjectSettings
from routes import api_router

app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version=ProjectSettings.API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ProjectSettings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)

# Root API
@app.get(ProjectSettings.API_VERSION_PATH, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Welcome to Sample Server"})

from db import dbconf, models, SessionLocal
from crud import crud_users, crud_base
from util import schemas
import uuid
# Server startup event
@app.on_event("startup")
def startup_event():
    print('startup event triggered')
    models.Base.metadata.create_all(bind=dbconf.engine)

    db = SessionLocal()

    uid = str(uuid.uuid4().hex)

    user = schemas.UserCreate
    user.id = uid
    user.email = "admin"
    user.password = "password"
    user.first_name = "admin"
    user.is_admin = True
    user.is_active = True
    user.created_by_userid = uid

    data = crud_base.get_user(email=user.email, db=db)
    if data is None:
        data = crud_users.create_user(user=user, db=db)