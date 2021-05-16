from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

users = {}

@router.post("/getToken")
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends())-> JSONResponse:

    # Checking if users in dict
    db_user = users[form_data.username] if form_data.username in users else None

    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        pass