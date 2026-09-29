from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
from auth import get_current_user
from llm_client import ask_gemini

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/proxy/draft")
def draft_proxy_message(
    recipient_label: str, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    spend_by_category = {}
    total_income = 0.0
    total_expense = 0.0
    for t in transactions:
        if t.type == "expense":
            spend_by_category[t.category] = spend_by_category.get(t.category, 0) + t.amount
            total_expense += t.amount
        elif t.type == "income":
            total_income += t.amount

    system_prompt = f"""
You draft a short, calm, judgment-free message a person can send to {recipient_label} about their
shared or personal finances. Keep it warm, non-accusatory, and no longer than 5 sentences.
Do not include a greeting/signature -- just the body text. Respond with ONLY the message text, nothing else.
""".strip()

    user_context = (
        f"Monthly income: ${total_income:.2f}\n"
        f"Monthly expenses: ${total_expense:.2f}\n"
        f"Spending by category: {spend_by_category}"
    )

    try:
        draft = ask_gemini(system_prompt, user_context, max_tokens=300)
    except Exception as err:
        raise HTTPException(502, f"Couldn't reach the AI service: {err}")

    # Note: this is returned as an editable draft only. Nothing is ever auto-sent.
    return {"draft": draft.strip(), "editable": True, "autoSent": False}
