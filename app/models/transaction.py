from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey, Date, Time
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..config.database import Base
from ..types import TransactionType, StatusType


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float(precision=2), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time(timezone=True), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=False)
    status = Column(
        Enum(StatusType, name="status_type", create_type=False),
        nullable=False,
    )
    notes = Column(String, nullable=False)
    transaction_type = Column(
        Enum(TransactionType, name="transaction_type", create_type=False),
        nullable=False,
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
