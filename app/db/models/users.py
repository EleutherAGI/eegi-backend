from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
from ..database import Base

from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    is_active = Column(Boolean, nullable=False)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)

    __mapper_args__ = {
        "polymorphic_identity" : "user",
        "polymorphic_on" : type
    }

class UserWithPasswordLogin(User):
    __tablename__ = "users_with_password_login"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    password_hash = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity' : 'user_with_password_login',
    }

# TODO User with github login