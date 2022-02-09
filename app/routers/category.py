from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..oauth2 import get_current_user
from ..config.database import get_db
from ..models.tags import Category
from ..schemas.category import (
    CategoryRequest,
    CreateCategoryResponse,
    FetchAllCategoriesResponse,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateCategoryResponse
)
async def create_category(
    category: CategoryRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        copied_category = category.dict().copy()
        copied_category["user_id"] = user.id

        new_category = Category(**copied_category)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to login.",
        )


@router.get("/", response_model=FetchAllCategoriesResponse)
async def fetch_categories(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = 20,
    page: int = 1,
):
    try:
        offset = (page - 1) * limit

        base_query = db.query(Category)
        where_query = (
            base_query.filter(Category.user_id == None)
            if user == None
            else base_query.filter(
                or_(Category.user_id == user.id, Category.user_id == None)
            )
        )

        categories = where_query.offset(offset).limit(limit).all()

        return {"categories": categories}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to fetch categories.",
        )
