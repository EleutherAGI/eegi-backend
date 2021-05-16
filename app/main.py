from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes import api_router

app = FastAPI()

API_VERSION_PATH = "/api/v1"

app.include_router(api_router, prefix=API_VERSION_PATH)

# Root API
@app.get(API_VERSION_PATH, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200,
                        content={
                            "message": "Welcome to Sample Server"})