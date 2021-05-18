from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from typing import Any


from db import models, pagination
from util import passutil, schemas
from crud import get_user


class CRUDKeys:
    def create_key(self, key: schemas.Registerkey, db: Session) -> Any:
        """ Add New User"""
        
        try:
            db_user = models.AccessKey(key_id=key.key,
                                  created_by_userid=key.created_by_userid)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            print(e)

    def get_key_id(self, id: int, db: Session) -> Any:
        """ Get Key Data based on id"""
        try:
            data = db.query(models.AccessKey).filter(
                models.AccessKey.key_id == id).first()
            return data
        except SQLAlchemyError as e:
            return None

    def get_all_keys(self, page_num: int, db: Session) -> Any:
        """ Get All Users"""
        try:
            # data = db.query(models.User).options(defer('password')).all()
            query = db.query(models.AccessKey).order_by(
                models.AccessKey.created_timestamp.desc())
            data = pagination.paginate(query=query, page=page_num,
                                       page_size=100)
            return data
        except SQLAlchemyError as e:
            return None
            
crud_keys = CRUDKeys()