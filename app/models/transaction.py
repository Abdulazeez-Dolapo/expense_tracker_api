import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Date, Time
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .tags import TransactionType
from ..config.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time(timezone=True), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=False)
    status = Column(String, nullable=False)
    notes = Column(String, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
