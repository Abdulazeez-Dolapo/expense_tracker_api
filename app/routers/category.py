from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session


from ..oauth2 import get_current_user, get_current_user_if_token
from ..config.database import get_db
from ..models.tags import Category
from ..schemas.category import (
    CategoryRequest,
    CreateCategoryResponse,
    FetchAllCategoriesResponse,
    FetchCategoryResponse,
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
    user: dict = Depends(get_current_user_if_token),
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    query = db.query(Category).filter(Category.id == id)

    category = query.first()

    if category == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id {id} not found",
        )

    if category.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete categories you created",
        )

    query.delete(synchronize_session=False)
    db.commit()

    return


@router.get("/{id}", response_model=FetchCategoryResponse)
async def fetch_category(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_if_token),
):
    query = db.query(Category).filter(Category.id == id)
    category = query.first()

    if category == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {id} not found",
        )

    if user == None:
        if category.user_id != None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You can only see default or categories you created",
            )
    else:
        if category.user_id != None and category.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You can only see default or categories you created",
            )

    return {"category": category}
