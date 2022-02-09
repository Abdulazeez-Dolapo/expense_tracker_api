from fastapi import Depends, status, HTTPException, Request
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config.env import environment_variables
from .config.database import get_db
from .models.user import User
from .schemas.user import TokenData


JWT_SECRET_KEY = environment_variables.JWT_SECRET_KEY
ALGORITHM = environment_variables.JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, time_to_expire: Optional[timedelta] = None):
    to_encode = data.copy()

    if time_to_expire:
        expire = datetime.utcnow() + timedelta(minutes=time_to_expire)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(
    token: str, credentials_exception: Exception, isAuthRequired: bool = True
):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None and isAuthRequired is True:
            raise credentials_exception

        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        if isAuthRequired is True:
            raise credentials_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter_by(id=token_data.id).first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_user_if_token(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception, False)
    user = (
        db.query(User).filter_by(id=token_data.id).first()
        if token_data != None
        else None
    )

    return user
