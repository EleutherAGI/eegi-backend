from sqlalchemy import Column, Boolean, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, validates
from ..dbconf import Base

from datetime import datetime

class AccessKey(Base):
    __tablename__ = "access_keys"

    key_id = Column(String, primary_key=True, index=True)
    is_admin = Column(Boolean)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    created_by_userid = Column(String, ForeignKey("users.id"), nullable=False)
    created_timestamp = Column(TIMESTAMP, nullable=False,
                               default=datetime.utcnow)

    created_by = relationship("User", 
            foreign_keys=[created_by_userid], 
            backref="created_by")
            
    used_by = relationship("User", 
            foreign_keys=[user_id], 
            backref="used_by")
