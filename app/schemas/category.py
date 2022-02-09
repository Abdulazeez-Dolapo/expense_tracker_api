from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..models.tags import TransactionType


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


class FetchAllCategoriesResponse(BaseModel):
    categories: List[Category]

    class Config:
        orm_mode = True


class FetchCategoryResponse(BaseModel):
    category: Category

    class Config:
        orm_mode = True
