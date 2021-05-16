from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import datetime
import uuid

import sys
sys.path.append("..")
from utils import deps, schemas
from crud import get_active_user, check_username_password, check_active_session, active_user, get_user
from settings import ProjectSettings
from auth import access_token

router = APIRouter()

@router.post("/getToken")
def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), 
                      db: Session = Depends(deps.get_db))-> JSONResponse:

    # Checking if users in dict
    db_user = get_active_user(email=form_data.username, db=db)

    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        is_password_correct = check_username_password(
            email=form_data.username,
            password=form_data.password,
            db=db)
        if is_password_correct is False:
            return JSONResponse(status_code=400,
                                content={"message": "Invalid Credentials"})
        else:
            access_token_expires = datetime.timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": form_data.username},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer"})

@router.get("/refreshToken")
def new_token(old_token: str = None, 
              session_id: str = None,
              db: Session = Depends(deps.get_db)) -> JSONResponse:
    
    if old_token and session_id:
        payload = access_token.decode_access_token(token=old_token)
        email = payload.get("sub")

        db_session = check_active_session(session_id=session_id, db=db)
        session_time = datetime.strptime(str(db_session.created_timestamp), "%Y-%m-%d %H:%M:%S.%f")
        diff = datetime.utcnow() - session_time
        limit = ProjectSettings.SESSION_TOKEN_EXPIRE_SECONDS  # 12 hours

        if email == db_session.email and (db_session.status == "logged_in" or db_session.status == "active") and diff.seconds < limit:
            active_user(session_id=session_id, db=db)
            access_token_expires = datetime.timedelta(minutes = ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": email},
                expires_delta=access_token_expires
            )
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                            "token_type": "Bearer"})
        else:
            return JSONResponse(status_code=400,
                                content={"message": "session ended"})
    else:
        return JSONResponse(status_code=400,
                            content={"message": "invalid token"})                                        

# replace response_model=Token with custom responses
@router.post("/login")
def login_user(user: schemas.UserLogin,
               db: Session = Depends(deps.get_db)) -> JSONResponse:
    """ Login user and Return Access Token"""
    db_user = get_active_user(email=user.email, db=db)
    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        is_password_correct = check_username_password(
            email=user.email,
            password=user.password,
            db=db)
        if is_password_correct is False:
            return JSONResponse(status_code=400,
                                content={"message": "Invalid Credentials"})
        else:
            uid = str(uuid.uuid4().hex)
            login_user(user=user, session_id=uid, db=db)
            access_token_expires = datetime.timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": user.email},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer",
                                         "session_id": uid,
                                         "user": jsonable_encoder(
                                             get_user(email=user.email,
                                                      db=db))})

@router.put("/logoff/{session_id}")
def logoff_user(session_id: str,
                db: Session = Depends(deps.get_db)) -> JSONResponse:
    """ Login user and Return Access Token"""
    db_session = logoff_user(session_id=session_id, db=db)
    if db_session is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})
