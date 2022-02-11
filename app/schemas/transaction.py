from typing import List
from datetime import date, time, datetime
from pydantic import BaseModel

from ..types import TransactionType, StatusType


class Transaction(BaseModel):
    id: int
    name: str
    amount: float
    date: date
    time: time
    category_id: int
    subcategory_id: int
    status: StatusType
    notes: str
    transaction_type: TransactionType
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateTransactionRequest(BaseModel):
    name: str
    amount: float
    date: date
    time: time
    category_id: int
    subcategory_id: int
    status: StatusType
    labels: List[int]
    notes: str
    transaction_type: TransactionType

    class Config:
        orm_mode = True


class CreateTransactionResponse(Transaction, BaseModel):
    class Config:
        orm_mode = True
