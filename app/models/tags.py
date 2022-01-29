import enum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..config.database import Base


class TransactionType(enum.Enum):
    Income = 1
    Expense = 2


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
    transaction_type = Column(Enum(TransactionType), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
