from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from ..database import Base

from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)

    __mapper_args___ = {
        "polymorphic_identity" : "user",
        "polymorphic_on": type
    }

class UserWithPasswordLogin(User):
    __tablename__ = "users_with_password_login"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    password_hash = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity':'manager',
    }

# TODO User with github login