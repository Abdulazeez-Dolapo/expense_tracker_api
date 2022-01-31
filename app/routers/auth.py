from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..config import database, env
from ..utils import hash_password, verify_password
from ..oauth2 import create_access_token
from ..models.user import User
from ..schemas.user import LoginResponse, RegisterResponse, RegisterRequest


ACCESS_TOKEN_EXPIRE_MINUTES = env.environment_variables.ACCESS_TOKEN_EXPIRY_IN_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    try:
        user = db.query(User).filter(User.email == user_credentials.username).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials"
            )

        isPasswordValid = verify_password(user_credentials.password, user.password)

        if not isPasswordValid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials"
            )

        token = create_access_token(
            data={"user_id": user.id}, time_to_expire=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to login.",
        )


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponse
)
async def register_user(user: RegisterRequest, db: Session = Depends(database.get_db)):
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password

        new_user = User(**user.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = create_access_token(
            data={"user_id": new_user.id}, time_to_expire=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return {"user_email": new_user.email, "access_token": access_token}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to register user.",
        )
