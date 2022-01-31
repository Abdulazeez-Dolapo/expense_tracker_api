from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class RegisterRequest(User, BaseModel):
    class Config:
        orm_mode = True


class RegisterResponse(BaseModel):
    user_email: str
    access_token: str

    class Config:
        orm_mode = True


class LoginResponse(Token, BaseModel):
    class Config:
        orm_mode = True
