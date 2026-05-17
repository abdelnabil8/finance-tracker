from pydantic import BaseModel
from enum import Enum

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class Transaction(BaseModel):
    title: str
    amount: float
    type: TransactionType
    category: str