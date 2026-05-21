from sqlalchemy import Column, Integer, String, Float, Enum
from pydantic import BaseModel
from enum import Enum as PyEnum
from pydantic import ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

# Pydantic schemas for auth
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str   