from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session


from ..oauth2 import get_current_user, get_current_user_if_token
from ..config.database import get_db
from ..models.tags import SubCategory, Category
from ..schemas.subcategory import (
    SubCategoryRequest,
    CreateSubCategoryResponse,
    FetchSubCategoriesResponse,
)

router = APIRouter(prefix="/subcategories", tags=["subcategories"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateSubCategoryResponse
)
async def create_subcategory(
    subcategory: SubCategoryRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    category = db.query(Category).filter(Category.id == subcategory.category_id).first()

    if category == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id {subcategory.category_id} does not exist.",
        )

    if category.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only add a subcategory to categories you created.",
        )

    copied_subcategory = subcategory.dict().copy()
    copied_subcategory["user_id"] = user.id

    new_subcategory = SubCategory(**copied_subcategory)

    db.add(new_subcategory)
    db.commit()
    db.refresh(new_subcategory)

    return new_subcategory


@router.get("/categories/{category_id}", response_model=FetchSubCategoriesResponse)
async def fetch_subcategories(
    category_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user_if_token),
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id {category_id} does not exist.",
        )

    print(user)
    if (user == None and category.user_id != None) or (
        user and category.user_id != user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only fetch subcategories of categories you created or default ones.",
        )

    subcategories = (
        db.query(SubCategory).filter(SubCategory.category_id == category_id).all()
    )

    return {"subcategories": subcategories}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(
    id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    query = db.query(SubCategory).filter(SubCategory.id == id)

    subcategory = query.first()

    if subcategory == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"subcategory with id {id} not found",
        )

    if subcategory.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete subcategories you created",
        )

    query.delete(synchronize_session=False)
    db.commit()

    return
