from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from ..config.database import Base


class TransactionLabel(Base):
    __tablename__ = "transaction_labels"

    id = Column(Integer, primary_key=True, nullable=False)
    label_id = Column(Integer, ForeignKey("labels.id"), nullable=True)
    transaction_id = Column(
        Integer, ForeignKey("transactions.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    label = relationship("Label", lazy="joined")
