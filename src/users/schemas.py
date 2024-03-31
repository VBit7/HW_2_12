import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi_users import schemas

# from src.entity.models import Role


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    # username: str
    username: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=12)

class UserUpdate(schemas.BaseUserUpdate):
    username: str


# GIT
# from pydantic import BaseModel, EmailStr, Field
#
#
# class UserSchema(BaseModel):
#     username: str = Field(min_length=2, max_length=50)
#     email: EmailStr
#     password: str = Field(min_length=6, max_length=12)
#
#
# class UserResponse(BaseModel):
#     id: int = 1
#     username: str
#     email: EmailStr
#     avatar: str
#
#     class Config:
#         from_attributes = True
#
#
# class TokenSchema(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str = "bearer"