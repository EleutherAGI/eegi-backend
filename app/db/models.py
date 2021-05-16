from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.types import Date
from .database import Base

from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)


class TextSample(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)


class TextComparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    text_id_1 = Column(Integer, nullable=False)
    text_id_2 = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    choice = Column(Integer(2), nullable=False) # Not sure if this 2 makes sense to use here
