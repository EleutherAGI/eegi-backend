from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from enum import Enum

from util import deps, schemas, response_schemas
from crud import crud_users, crud_base

router = APIRouter()


class UserStatus(str, Enum):
    enable = "enable"
    disable = "disable"


@router.post("/", responses=response_schemas.general_responses)
def register_user(user: schemas.AdminUserCreate,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_admin)) -> JSONResponse:
    """ Register A User"""
    data = crud_base.get_user(email=user.email, db=db)


    if data is not None:
        return JSONResponse(status_code=400,
                            content={"message": "email already registered"})
    data = crud_users.create_user(user=user, created_by_userid=current_user.id, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/{user_id}", responses=response_schemas.general_responses)
def update_user(user_id: str, user: schemas.UserUpdate,
                db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_admin)) -> JSONResponse:
    """ Update A User"""

    data = crud_users.update_user(user_id=user_id, user=user, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/change_password/{user_id}",
            responses=response_schemas.general_responses,
            include_in_schema=False)
def update_password(user_id: str, user: schemas.UserPasswordChange,
                    db: Session = Depends(deps.get_db),
                    current_user: schemas.UserVerify = Depends(
                        deps.get_current_admin)) -> JSONResponse:
    """ Update User Password"""
    is_password_correct = crud_users.check_password(user_id=user_id,
                                                    password=user.password,
                                                    db=db)
    if is_password_correct is False:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid password"})

    data = crud_users.change_user_password(user_id=user_id,
                                           password=user.new_password, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})

    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("/user_status/{user_id}",
            responses=response_schemas.general_responses)
def update_user_status(user_id: str, status: UserStatus = UserStatus.enable,
                       db: Session = Depends(deps.get_db),
                       current_user: schemas.UserVerify = Depends(
                           deps.get_current_admin)) -> JSONResponse:
    """ Update A User Status """

    data = crud_users.user_status_update(user_id=user_id, status=status, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.delete("/{user_id}",
               responses=response_schemas.general_responses)
def delete_user(user_id: str, db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_admin)) -> JSONResponse:
    """ Delete A User"""
    data = crud_users.delete_user(user_id=user_id, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("/", responses=response_schemas.all_users_responses)
def get_users(user_id: str = None, page_num: int = 1,
              db: Session = Depends(deps.get_db),
              current_user: schemas.UserVerify = Depends(
                  deps.get_current_admin)) -> JSONResponse:
    """ Return All Users"""
    if user_id is not None:
        db_user = crud_users.get_user_id(id=user_id, db=db)
        if db_user is None:
            return JSONResponse(status_code=500,
                                content={"message": "No User Found"})
        json_compatible_item_data = jsonable_encoder(db_user)
        return JSONResponse(status_code=200,
                            content=json_compatible_item_data)
    else:
        db_user = crud_users.get_all_user(page_num=page_num, db=db)
        if db_user is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Users Found"})
        json_compatible_item_data = jsonable_encoder(db_user)
        return JSONResponse(status_code=200,
                            content={"total_pages": db_user.pages,
                                     "total_items": db_user.total_items,
                                     "page_data": {"page_num": page_num,
                                                   "item_count": db_user.page_size,
                                                   "items":
                                                       json_compatible_item_data}})