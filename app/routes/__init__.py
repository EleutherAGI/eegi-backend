from fastapi import APIRouter
from . import users
from . import keys
from . import login
from . import filter

api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["Admin"])
api_router.include_router(keys.router, prefix="/keys", tags=["Admin"])
api_router.include_router(filter.router, prefix="/filter", tags=["Labeling"])
api_router.include_router(login.router, tags=["Login"])
