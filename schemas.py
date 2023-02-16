from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


# request post schema
class RequestPostSchema(BaseModel):
    title: str
    content: str


# response user create schema
class ResponseUserCreateSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# response post schema
class ResponsePostSchema(BaseModel):
    # use inheritance to have all the columns of the post response model, refrain from creating the columns manually.
    # Just to have more clarity of what we are doing, I am going to use the manual way of doing it, but I'll advise my
    # futureself to use inheritance.
    title: str
    content: str
    owner_id: int
    owner_info: ResponseUserCreateSchema

    # this commands tells pydantic to convert the sqlalchemy model into a valid dictionary, because pydantic works with
    # dictionaries
    class Config:
        orm_mode = True


# request user create schema
class RequestUserCreateSchema(BaseModel):
    email: EmailStr
    password: str


# this schema will be used for having email and password from the user
class RequestUserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

