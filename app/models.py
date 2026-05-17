from sqlalchemy import Column, Integer, String, Float, Enum
from pydantic import BaseModel
from enum import Enum as PyEnum
from app.database import Base

# --- SQLAlchemy Model (Database Table) ---
class TransactionType(str, PyEnum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, nullable=False)

# --- Pydantic Model (API Validation) ---
class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: TransactionType
    category: str

class TransactionResponse(TransactionCreate):
    id: int
    class Config:
        from_attributes = True