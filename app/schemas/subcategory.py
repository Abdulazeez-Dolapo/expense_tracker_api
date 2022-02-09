from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..models.tags import TransactionType


class SubCategory(BaseModel):
    id: int
    name: str
    user_id: Optional[int]
    category_id: int
    transaction_type: TransactionType
    created_at: datetime

    class Config:
        orm_mode = True


class SubCategoryRequest(BaseModel):
    name: str
    transaction_type: TransactionType
    category_id: int


class CreateSubCategoryResponse(SubCategory, BaseModel):
    class Config:
        orm_mode = True


class FetchSubCategoriesResponse(BaseModel):
    subcategories: List[SubCategory]

    class Config:
        orm_mode = True


# class FetchCategoryResponse(BaseModel):
#     category: Category

#     class Config:
#         orm_mode = True
