from pydantic import BaseModel
from sqlalchemy.sql.expression import text


# ---------------- login schemas -------------------- #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    expire: str = None
    issue_time: str = None


# ---------------- login schemas -------------------- #
class UserBase(BaseModel):
    email: str


class UserVerify(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
    first_name: str
    is_active: bool = True
    is_admin: bool = False
    created_by_userid: str

class UserKeyCreate(UserBase):
    password: str
    first_name: str
    key: str


class UserUpdate(BaseModel):
    first_name: str
    is_active: bool = True
    is_admin: bool = False


class UserPasswordChange(BaseModel):
    password: str
    new_password: str



class UserAuthenticate(UserBase):
    password: str


class UserLogIn(UserBase):
    password: str


class UserPasswordReset(BaseModel):
    token: str
    password: str


# return in response
class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Key(BaseModel):
    key: str
    is_admin: bool

class FilterSampleCreate(BaseModel):
    text_sample_id_1: str
    text_sample_id_2: str
    user_id: str
    
class ComparisonUpdate(BaseModel):
    id: str
    item_1_is_better: bool
    