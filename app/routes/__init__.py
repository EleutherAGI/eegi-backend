from fastapi import APIRouter
from . import admin
from . import keys
from . import login
from . import articles

api_router = APIRouter()


api_router.include_router(admin.router, prefix="/users", tags=["Admin"])
api_router.include_router(keys.router, prefix="/keys", tags=["Admin"])
api_router.include_router(articles.router, prefix="/articles",
                          tags=["Texts"])
api_router.include_router(login.router, tags=["Login"])
