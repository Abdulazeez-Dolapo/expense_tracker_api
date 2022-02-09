from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..oauth2 import get_current_user
from ..config.database import get_db
from ..models.tags import Label
from ..schemas.label import LabelRequest, CreateLabelResponse, FetchAllLabelsResponse

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


@router.get("/", response_model=FetchAllLabelsResponse)
async def fetch_all_labels(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = 20,
    page: int = 1,
):
    try:
        offset = (page - 1) * limit

        base_query = db.query(Label)
        where_query = (
            base_query.filter(Label.user_id == None)
            if user == None
            else base_query.filter(or_(Label.user_id == user.id, Label.user_id == None))
        )

        labels = where_query.offset(offset).limit(limit).all()

        return {"labels": labels}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to fetch labels.",
        )
