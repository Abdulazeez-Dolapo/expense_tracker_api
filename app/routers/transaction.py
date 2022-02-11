from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session


from ..oauth2 import get_current_user
from ..config.database import get_db
from ..models.transaction import Transaction
from ..models.transaction_label import TransactionLabel
from ..schemas.transaction import CreateTransactionRequest, CreateTransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateTransactionResponse
)
async def create_transaction(
    transaction: CreateTransactionRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    try:
        copied_transaction = transaction.dict().copy()
        labels = copied_transaction["labels"]
        del copied_transaction["labels"]
        copied_transaction["user_id"] = user.id

        new_transaction = Transaction(**copied_transaction)

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        if new_transaction != None:
            new_transaction_label = []

            for label_id in labels:
                new_transaction_label.append(
                    {"label_id": label_id, "transaction_id": new_transaction.id}
                )

            db.bulk_insert_mappings(TransactionLabel, new_transaction_label)
            db.commit()

        return new_transaction

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to create a transaction.",
        )
