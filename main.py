from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, SessionLocal, Base
from models import User, Transaction, Budget
from auth import hash_password, verify_password, create_token, get_current_user
from chatbot import ask_finance_bot

# Part 2 routers
import financial_diary
import regret_mining
import fire_drills
import proxy_mode

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Personal Finance Advisor Chatbot")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Feature 1: Auth ----------

@app.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "signup successful"}


@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_token(user.id)
    return {"token": token, "user_id": user.id}


# ---------- Features 2, 3, 5: Transactions ----------
# Note: user_id is now taken from the verified token (get_current_user), never from the
# request itself -- this is the data-isolation fix mentioned when we found the gap.

@app.post("/transactions")
def add_transaction(
    amount: float,
    category: str,
    type: str,
    merchant: str = None,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if type not in ("expense", "income"):
        raise HTTPException(400, "type must be 'expense' or 'income'")
    txn = Transaction(user_id=user_id, amount=amount, category=category, type=type, merchant=merchant, date=datetime.now())
    db.add(txn)
    db.commit()
    return {"message": "transaction added", "id": txn.id}


@app.get("/transactions")
def get_transactions(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


# ---------- Feature 4: Budgets ----------

@app.post("/budgets")
def set_budget(
    category: str, limit_amount: float, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    existing = db.query(Budget).filter(Budget.user_id == user_id, Budget.category == category).first()
    if existing:
        existing.limit_amount = limit_amount
    else:
        db.add(Budget(user_id=user_id, category=category, limit_amount=limit_amount))
    db.commit()
    return {"message": "budget set"}


@app.get("/budgets/status/{category}")
def check_budget(category: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    spent = sum(
        t.amount
        for t in db.query(Transaction)
        .filter(Transaction.user_id == user_id, Transaction.category == category, Transaction.type == "expense")
        .all()
    )
    budget = db.query(Budget).filter(Budget.user_id == user_id, Budget.category == category).first()
    if not budget:
        return {"message": "no budget set"}
    return {"spent": spent, "limit": budget.limit_amount, "over_budget": spent > budget.limit_amount}


# ---------- Feature 6: Conversational Interface ----------

@app.post("/chat")
def chat(question: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        answer = ask_finance_bot(question, db, user_id)
    except Exception as err:
        raise HTTPException(502, f"Couldn't reach the AI service: {err}")
    return {"answer": answer}


# ---------- Feature 7: Dashboard ----------

@app.get("/dashboard")
def dashboard(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    by_category = {}
    for t in transactions:
        if t.type == "expense":
            by_category[t.category] = by_category.get(t.category, 0) + t.amount
    return {"total_income": total_income, "total_expense": total_expense, "by_category": by_category}


# ---------- Part 2: Creative extensions ----------

app.include_router(financial_diary.router, tags=["Idea 1: Financial Diary"])
app.include_router(regret_mining.router, tags=["Idea 2: Regret Mining"])
app.include_router(fire_drills.router, tags=["Idea 3: Fire Drills"])
app.include_router(proxy_mode.router, tags=["Idea 4: Proxy Mode"])
