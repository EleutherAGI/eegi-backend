from typing import Optional

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    expire: str = None
    issue_time: str = None

# base user properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    first_name: Optional[str] = None

# properties when creating new user
class UserLogin(UserBase):
    email: EmailStr
    password: str

class UserVerify(UserBase):
    id: int


# base properties
class ComparisonBase(BaseModel):
    text1: str = None
    text2: str = None
    choice: Optional[str] = None