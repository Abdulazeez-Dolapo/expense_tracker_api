from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..oauth2 import get_current_user
from ..config.database import get_db
from ..models.transaction import Transaction
from ..models.transaction_label import TransactionLabel
from ..schemas.transaction import (
    CreateTransactionRequest,
    CreateTransactionResponse,
    EditTransactionRequest,
    FetchTransactionResponse,
    FetchAllTransactionsResponse,
    CreateTransactionLabelRequest,
    CreateTransactionLabelResponse,
)

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


@router.put("/{id}", response_model=CreateTransactionResponse)
async def update_transaction(
    id: int,
    transaction: EditTransactionRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    transaction_query = db.query(Transaction).filter(Transaction.id == id)
    stored_transaction = transaction_query.first()

    if stored_transaction == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {id} not found",
        )

    if stored_transaction.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only edit transactions you created",
        )

    try:
        transaction_query.update(transaction.dict(), synchronize_session=False)
        db.commit()

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to update the transaction.",
        )

    return stored_transaction


@router.get("/{id}", response_model=FetchTransactionResponse)
async def fetch_transaction(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    query = (
        db.query(Transaction)
        .join(
            TransactionLabel,
            TransactionLabel.transaction_id == Transaction.id,
            isouter=True,
        )
        .filter(Transaction.id == id)
    )

    transaction = query.first()

    if transaction == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"transaction with id {id} not found",
        )

    if transaction.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only see transactions you created",
        )

    return transaction


@router.get("/", response_model=FetchAllTransactionsResponse)
async def fetch_transactions(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    limit: int = 20,
    page: int = 1,
):
    try:
        offset = (page - 1) * limit

        query = db.query(Transaction).join(
            TransactionLabel,
            TransactionLabel.transaction_id == Transaction.id,
            isouter=True,
        )

        transactions = (
            query.filter(Transaction.user_id == user.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {"transactions": transactions}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to fetch transactions.",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)
):
    query = db.query(Transaction).filter(Transaction.id == id)

    transaction = query.first()

    if transaction == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {id} not found",
        )

    if transaction.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete transactions you created",
        )

    query.delete(synchronize_session=False)
    db.commit()

    return


@router.post(
    "/transaction_labels",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTransactionLabelResponse,
)
async def create_transaction_labels(
    transaction_label: CreateTransactionLabelRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):

    copied_transaction_label = transaction_label.dict().copy()

    labels = copied_transaction_label["labels"]
    transaction_id = copied_transaction_label["transaction_id"]

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if transaction == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id {transaction_id} not found",
        )

    if transaction.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only add labels to transactions you created",
        )

    try:
        db.query(TransactionLabel).filter(
            TransactionLabel.transaction_id == transaction_id
        ).delete(synchronize_session=False)

        new_transaction_label = []

        for label_id in labels:
            new_transaction_label.append(
                {"label_id": label_id, "transaction_id": transaction_id}
            )

        db.bulk_insert_mappings(TransactionLabel, new_transaction_label)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while trying to delete or add to the TransactionLabel.",
        )

    return {"message": "Labels added successfully."}
