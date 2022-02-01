from datetime import datetime
from pydantic import BaseModel


class Label(BaseModel):
    id: int
    name: str
    user_id: int
    created_at: datetime


class LabelRequest(BaseModel):
    name: str


class CreateLabelResponse(Label, BaseModel):
    class Config:
        orm_mode = True
