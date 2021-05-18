from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..dbconf import Base

from datetime import datetime

class AccessKey(Base):
    __tablename__ = "access_keys"

    key_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    created_by_userid = Column(Integer, nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)
