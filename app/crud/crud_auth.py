from sqlalchemy.orm import Session, defer
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from sqlalchemy.sql import expression
from typing import Any

import sys

sys.path.append("..")
from db import models
from utils import schemas

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"],
                           deprecated=["md5_crypt", "des_crypt"])

def get_user(email: str, db: Session) -> Any:
    try:
        data = db.query(models.User).filter(models.User.email == email).options(defer('password')).first()
        return data
    except SQLAlchemyError as e:
        return None


def get_active_user(email: str, db: Session) -> Any:
    try:
        data = db.query(models.User).filter(models.User.email == email, 
        models.User.is_active == expression.true()).options(defer('password')).first()
        return data
    except SQLAlchemyError as e:
        return None


def check_username_password(email: str, password: str,
                            db: Session) -> Any:
    db_user_info = get_user(email=email, db=db)

    return pwd_context.verify(str(password),
                              str(db_user_info.password))


def check_active_session(session_id: str,
                            db: Session):
    try:
        db_session = db.query(models.UsersLoginAttempt).filter(
            models.UsersLoginAttempt.session_id == session_id).first()
        return db_session
    except SQLAlchemyError as e:
        return None


def login_user(user: schemas.UserLogin, session_id: str,
                db: Session) -> Any:
    try:
        db_session = models.UsersLoginAttempt(
            email=user.email,
            session_id=session_id,
            status="logged_in")
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        return None


def active_user(self, session_id: str,
                db: Session) -> Any:
    """ check for active user"""
    try:
        db_session = db.query(models.UsersLoginAttempt).filter(
            models.UsersLoginAttempt.session_id == session_id).first()

        db_session.status = "active"
        db.commit()
        db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        return None


def logoff_user(self, session_id: str,
                db: Session) -> Any:
    """ Logging off Record"""
    try:
        db_session = db.query(models.UsersLoginAttempt).filter(
            models.UsersLoginAttempt.session_id == session_id).first()

        db_session.status = "logged_off"
        db.commit()
        db.refresh(db_session)
        return db_session
    except SQLAlchemyError as e:
        return None