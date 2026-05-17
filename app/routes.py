from fastapi import APIRouter
from app.models import Transaction, TransactionType

router = APIRouter()

# In-memory list (no database yet)
transactions = []

@router.get("/")
def get_transactions():
    return transactions

@router.post("/")
def create_transaction(transaction: Transaction):
    transactions.append(transaction.dict())
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int):
    if transaction_id >= len(transactions) or transaction_id < 0:
        return {"error": "Transaction not found"}
    transactions.pop(transaction_id)
    return {"message": "Deleted successfully"}