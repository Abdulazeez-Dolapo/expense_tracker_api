from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class Label(BaseModel):
    id: int
    name: str
    user_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class LabelRequest(BaseModel):
    name: str


class CreateLabelResponse(Label, BaseModel):
    class Config:
        orm_mode = True


class FetchAllLabelsResponse(BaseModel):
    labels: List[Label]

    class Config:
        orm_mode = True
