from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..models.tags import TransactionType
from ..schemas.subcategory import SubCategory


class Category(BaseModel):
    id: int
    name: str
    user_id: Optional[int]
    created_at: datetime
    transaction_type: TransactionType

    class Config:
        orm_mode = True


class CategoryRequest(BaseModel):
    name: str
    transaction_type: TransactionType


class CreateCategoryResponse(Category, BaseModel):
    class Config:
        orm_mode = True


class FullCategory(Category):
    subcategories: List[SubCategory]

    class Config:
        orm_mode = True


class FetchAllCategoriesResponse(BaseModel):
    categories: List[FullCategory]

    class Config:
        orm_mode = True


class FetchCategoryResponse(BaseModel):
    category: FullCategory

    class Config:
        orm_mode = True


class CategoryUpdateRequest(BaseModel):
    name: str
    transaction_type: TransactionType

    class Config:
        orm_mode = True
