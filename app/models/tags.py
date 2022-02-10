import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from ..config.database import Base


class TransactionType(enum.Enum):
    Income = "Income"
    Expense = "Expense"


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    transaction_type = Column(
        Enum(TransactionType, name="transaction_type", create_type=False),
        nullable=False,
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    subcategories = relationship("SubCategory", lazy="joined")


class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    transaction_type = Column(
        Enum(TransactionType, name="transaction_type", create_type=False),
        nullable=False,
    )
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
