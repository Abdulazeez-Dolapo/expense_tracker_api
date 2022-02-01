from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..oauth2 import get_current_user
from ..config.database import get_db
from ..models.tags import Label
from ..schemas.label import LabelRequest, CreateLabelResponse

router = APIRouter(prefix="/labels", tags=["labels"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateLabelResponse
)
async def create_label(
    label: LabelRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        copied_label = label.dict().copy()
        copied_label["user_id"] = user.id

        new_label = Label(**copied_label)

        db.add(new_label)
        db.commit()
        db.refresh(new_label)

        return new_label

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to login.",
        )
