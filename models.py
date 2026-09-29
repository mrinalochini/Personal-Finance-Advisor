from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    category = Column(String)
    type = Column(String)  # "expense" or "income"
    merchant = Column(String, nullable=True)
    date = Column(DateTime)
    # Added for Part 2:
    mood = Column(String, nullable=True)      # Idea 1: Financial Diary
    regret = Column(Boolean, nullable=True)   # Idea 2: Regret Mining


class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    limit_amount = Column(Float)
