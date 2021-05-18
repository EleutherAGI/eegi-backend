from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from ..dbconf import Base

from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    created_by_userid = Column(Integer, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=True,
                            default=datetime.utcnow)

class UsersLoginAttempt(Base):
    __tablename__ = "user_login_attempt"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)