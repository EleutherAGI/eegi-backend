from fastapi import APIRouter
from . import login
from . import comparisons

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(comparisons.router, prefix="/comparisons", tags=["Compare"])