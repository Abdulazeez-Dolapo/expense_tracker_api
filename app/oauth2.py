from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

from .config.env import environment_variables


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
