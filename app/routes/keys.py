from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from enum import Enum
import uuid

from util import deps, schemas
from crud import crud_keys
from util import response_schemas

router = APIRouter()


class UserStatus(str, Enum):
    enable = "enable"
    disable = "disable"


@router.post("/", responses=response_schemas.general_responses)
def register_key(key: schemas.Key,
                  db: Session = Depends(deps.get_db),
                  current_user: schemas.UserVerify = Depends(
                      deps.get_current_admin)) -> JSONResponse:
    """ Create A Key, If nothing is provided will return a uuid"""
    
    new_key = schemas.Registerkey
    new_key.created_by_userid = current_user.id
    new_key.key = key.key if key.key is not None else str(uuid.uuid4().hex)
    
    data = crud_keys.create_key(key=new_key, db=db)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("/", responses=response_schemas.all_keys_responses)
def get_keys(key_id: str = None, page_num: int = 1,
              db: Session = Depends(deps.get_db),
              current_user: schemas.UserVerify = Depends(
                  deps.get_current_admin)) -> JSONResponse:
    """ Return All Keys"""
    if key_id is not None:
        db_key = crud_keys.get_key_id(id=key_id, db=db)
        if db_key is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Key Found"})
        json_compatible_item_data = jsonable_encoder(db_key)
        return JSONResponse(status_code=200,
                            content=json_compatible_item_data)
    else:
        db_key = crud_keys.get_all_keys(page_num=page_num, db=db)
        if db_key is None:
            return JSONResponse(status_code=500,
                                content={"message": "No Keys Found"})
        json_compatible_item_data = jsonable_encoder(db_key)
        return JSONResponse(status_code=200,
                            content={"total_pages": db_key.pages,
                                     "total_items": db_key.total_items,
                                     "page_data": {"page_num": page_num,
                                                   "item_count": db_key.page_size,
                                                   "items":
                                                       json_compatible_item_data}})