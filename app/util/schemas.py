from pydantic import BaseModel


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
    created_by_userid: int

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


# Request body classes
class RedisRq(BaseModel):
    range_value: int


class ArticleCreate(BaseModel):
    user_id: int
    article_title: str
    article_text: str
    tags: list


class ArticleUpdate(BaseModel):
    user_id: int
    article_title: str
    article_text: str
    tags: list


class Key(BaseModel):
    key: str = None

class Registerkey(Key):
    created_by_userid: int