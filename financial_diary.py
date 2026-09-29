from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
from auth import get_current_user
from llm_client import ask_gemini_for_json

router = APIRouter()

EXTRACT_SYSTEM_PROMPT = """
You extract structured transaction data from a short diary-style note about a purchase.
Respond with ONLY a JSON object, no other text, in this exact shape:
{
  "amount": <number, in dollars, your best guess if not stated exactly>,
  "category": <one of: "food", "shopping", "entertainment", "bills", "transport", "other">,
  "merchant": <string, best guess or "unknown">,
  "mood": <one word describing the emotional state implied, e.g. "guilty", "happy", "stressed", "neutral">
}
""".strip()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/diary/parse")
def parse_diary_entry(note: str, user_id: int = Depends(get_current_user)):
    """Step 1: parse a diary entry into structured data (does NOT save yet)."""
    try:
        parsed = ask_gemini_for_json(EXTRACT_SYSTEM_PROMPT, note)
    except Exception as err:
        raise HTTPException(502, f"Couldn't reach the AI service: {err}")
    return {"parsed": parsed, "originalNote": note}


@router.post("/diary/confirm")
def confirm_diary_entry(
    amount: float,
    category: str,
    mood: str = "neutral",
    merchant: str = "unknown",
    note: str = "",
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Step 2: user confirms (possibly edits) the parsed data -> actually save it."""
    txn = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        type="expense",
        merchant=merchant,
        mood=mood,
        date=datetime.now(),
    )
    db.add(txn)
    db.commit()
    return {"id": txn.id, "saved": True}


@router.get("/diary/insight")
def diary_insight(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Group recent transactions by mood and surface a pattern."""
    transactions = (
        db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.mood.isnot(None)).all()
    )
    if not transactions:
        return {"insight": "Not enough diary entries yet to spot a pattern."}

    by_mood = {}
    for t in transactions:
        entry = by_mood.setdefault(t.mood, {"count": 0, "total": 0.0, "categories": {}})
        entry["count"] += 1
        entry["total"] += t.amount
        entry["categories"][t.category] = entry["categories"].get(t.category, 0) + 1

    top_mood, data = max(by_mood.items(), key=lambda kv: kv[1]["total"])
    top_category = max(data["categories"].items(), key=lambda kv: kv[1])[0]

    return {
        "insight": (
            f"You tend to spend the most on {top_category} when you're feeling "
            f"{top_mood} (${data['total']:.2f} across {data['count']} entries)."
        )
    }
