from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


from ..config.database import Base


class TransactionLabels(Base):
    __tablename__ = "transaction_labels"

    id = Column(Integer, primary_key=True, nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
