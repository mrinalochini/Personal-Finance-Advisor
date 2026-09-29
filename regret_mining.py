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


@router.get("/regret/retro")
def regret_retro(limit: int = 20, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Onboarding 'regret retro': fetch the user's last N transactions to react to."""
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id, Transaction.type == "expense")
        .order_by(Transaction.date.desc())
        .limit(limit)
        .all()
    )
    return {
        "transactions": [
            {"id": t.id, "amount": t.amount, "category": t.category, "merchant": t.merchant, "date": t.date}
            for t in transactions
        ]
    }


@router.post("/regret/tag")
def tag_regret(
    transaction_id: int, regret: bool, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Tag a single transaction as regretted or not (scoped to the authenticated user)."""
    txn = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .first()
    )
    if not txn:
        raise HTTPException(404, "Transaction not found.")
    txn.regret = regret
    db.commit()
    return {"saved": True}


@router.get("/regret/suggested-budgets")
def suggested_budgets(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Compute derived budget suggestions per category from regretted transactions."""
    regretted = db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.regret == True).all()

    if not regretted:
        return {"suggestions": [], "message": "No regretted transactions tagged yet."}

    by_category = {}
    for t in regretted:
        by_category.setdefault(t.category, []).append(t.amount)

    suggestions = []
    for category, amounts in by_category.items():
        avg = sum(amounts) / len(amounts)
        suggested_limit = round(avg * 0.8)

        try:
            phrasing = ask_gemini(
                "You write one short, encouraging sentence suggesting a monthly budget cap "
                "based on the user's own past regretted purchases. No preamble, just the sentence.",
                f"Category: {category}. Average regretted purchase: ${avg:.2f}. Suggested cap: ${suggested_limit}.",
                max_tokens=100,
            )
        except Exception as err:
            raise HTTPException(502, f"Couldn't reach the AI service: {err}")

        suggestions.append({"category": category,"suggestedLimit": suggested_limit,"phrasing": (phrasing or f"Consider setting a monthly {category} budget of {suggested_limit}.").strip()})
    return {"suggestions": suggestions}
