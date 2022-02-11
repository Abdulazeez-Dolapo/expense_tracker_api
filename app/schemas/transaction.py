from typing import List
from datetime import date, time, datetime
from pydantic import BaseModel

from ..types import TransactionType, StatusType
from .label import Label


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


class TransactionLabel(BaseModel):
    id: int
    label_id: int
    transaction_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionRequest(BaseModel):
    name: str
    amount: float
    date: date
    time: time
    category_id: int
    subcategory_id: int
    status: StatusType
    notes: str
    transaction_type: TransactionType

    class Config:
        orm_mode = True


class CreateTransactionRequest(TransactionRequest, BaseModel):
    labels: List[int]

    class Config:
        orm_mode = True


class EditTransactionRequest(TransactionRequest, BaseModel):
    class Config:
        orm_mode = True


class CreateTransactionResponse(Transaction, BaseModel):
    class Config:
        orm_mode = True


class FullLabel(TransactionLabel, BaseModel):
    label: Label


class FetchTransactionResponse(Transaction, BaseModel):
    labels: List[FullLabel]

    class Config:
        orm_mode = True
