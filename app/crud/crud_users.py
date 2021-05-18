from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import defer
from datetime import datetime
from typing import Any
import sys

sys.path.append("..")
from db import models, pagination
from util import passutil, schemas
import uuid


class CRUDUsers:
    def create_user_from_key(self, user: schemas.UserCreate, key: str, db: Session) -> Any:
        """ Add New User"""
        
        try:
            hashed_password = passutil.get_password_hash(str(user.password))
            db_user = models.User(id=str(uuid.uuid4().hex),
                                  email=user.email,
                                  hashed_password=hashed_password,
                                  first_name=user.first_name,
                                  is_active=user.is_active,
                                  is_admin=user.is_admin,
                                  created_by_userid=user.created_by_userid)
            
            db_key = db.query(models.AccessKey).filter(
                models.AccessKey.key_id == key).first()

            db_key.user_id = db_user.id
            print(db_key.user_id)

            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            db.refresh(db_key)
            return db_user
        except SQLAlchemyError as e:
            print(e)


    def create_user(self, user: schemas.UserCreate, db: Session) -> Any:
        """ Add New User"""
        
        try:
            hashed_password = passutil.get_password_hash(str(user.password))
            db_user = models.User(id=str(uuid.uuid4().hex),
                                  email=user.email,
                                  hashed_password=hashed_password,
                                  first_name=user.first_name,
                                  is_active=user.is_active,
                                  is_admin=user.is_admin,
                                  created_by_userid=user.created_by_userid)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            print(e)

    def update_user(self, user_id: int, user: schemas.UserUpdate,
                    db: Session) -> Any:
        """ Update User"""
        try:
            
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()

            db_user.first_name = user.first_name
            db_user.is_active = user.is_active
            db_user.is_admin = user.is_admin

            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def check_password(self, user_id: int, password: str,
                       db: Session):
        """ get user Password"""
        try:
            db_user = db.query(models.User.password).filter(
                models.User.id == user_id).first()
            return passutil.verify_password(str(password),
                                            str(db_user.password))
        except SQLAlchemyError as e:
            return None

    def change_user_password(self, user_id: str, password: str,
                             db: Session) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()
            db_user.hashed_password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def update_user_password(self, email: str, password: str,
                             db: Session) -> Any:
        """ Update User Password"""
        try:
            hashed_password = passutil.get_password_hash(password)
            db_user = db.query(models.User).filter(
                models.User.email == email).first()
            db_user.hashed_password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def delete_user(self, user_id: int, db: Session) -> Any:
        """ Delete User"""
        try:
            db.query(models.User).filter(
                models.User.id == user_id).delete()
            db.commit()
            return True
        except SQLAlchemyError as e:
            return None

    def user_status_update(self, user_id: int, status: str,
                           db: Session) -> Any:
        """ Disable User"""
        try:
            db_user = db.query(models.User).filter(
                models.User.id == user_id).first()
            if status == "enable":
                db_user.is_active = True
            elif status == "disable":
                db_user.is_active = False
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            return None

    def verify_user(self, email: str, db: Session) -> Any:
        """ Verify User"""
        try:
            data = db.query(models.User.id, models.User.email, models.User.is_admin).filter(
                models.User.email == email).first()
            return data
        except SQLAlchemyError as e:
            return None

    def get_user_id(self, id: int, db: Session) -> Any:
        """ Get User Data based on id"""
        try:
            data = db.query(models.User).filter(
                models.User.id == id).options(defer('hashed_password')).first()
            return data
        except SQLAlchemyError as e:
            return None

    # https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred
    def get_all_user(self, page_num: int, db: Session) -> Any:
        """ Get All Users"""
        try:
            # data = db.query(models.User).options(defer('password')).all()
            query = db.query(models.User).options(
                defer('hashed_password')).order_by(
                models.User.created_timestamp.desc())
            data = pagination.paginate(query=query, page=page_num,
                                       page_size=100)
            return data
        except SQLAlchemyError as e:
            return None


crud_users = CRUDUsers()
