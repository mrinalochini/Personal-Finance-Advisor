from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
from auth import get_current_user
from llm_client import ask_gemini_for_json

router = APIRouter()

SCENARIOS = {
    "rent_increase": {
        "id": "rent_increase",
        "prompt": "Your landlord just told you rent is going up $200/month starting next month. "
        "Walk me through what you'd cut or change.",
    },
    "medical_bill": {
        "id": "medical_bill",
        "prompt": "You just got a surprise $350 medical bill due in two weeks. What's your plan to cover it?",
    },
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/firedrill/scenario/{scenario_id}")
def get_scenario(scenario_id: str):
    scenario = SCENARIOS.get(scenario_id)
    if not scenario:
        raise HTTPException(404, "Unknown scenario.")
    return {"drill": True, **scenario}


@router.post("/firedrill/respond")
def respond_to_drill(
    scenario_id: str,
    user_plan: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    scenario = SCENARIOS.get(scenario_id)
    if not scenario:
        raise HTTPException(404, "Unknown scenario.")

    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    spend_by_category = {}
    total_income = 0.0
    for t in transactions:
        if t.type == "expense":
            spend_by_category[t.category] = spend_by_category.get(t.category, 0) + t.amount
        elif t.type == "income":
            total_income += t.amount

    scoring_prompt = """
You are scoring whether a user's stated financial plan would realistically cover a surprise expense,
given their real spending data. Respond with ONLY a JSON object in this exact shape:
{
  "feasible_percent": <integer 0-100, how much of the gap their plan would realistically cover>,
  "verdict": <one short sentence, encouraging but honest>,
  "suggestion": <one short sentence with a concrete alternative if their plan falls short>
}
""".strip()

    user_context = (
        f'Scenario: {scenario["prompt"]}\n'
        f'User\'s stated plan: "{user_plan}"\n'
        f"User's monthly income: ${total_income:.2f}\n"
        f"User's spending by category: {spend_by_category}"
    )

    try:
        result = ask_gemini_for_json(scoring_prompt, user_context, max_tokens=300)
    except Exception as err:
        raise HTTPException(502, f"Couldn't reach the AI service: {err}")

    return {"drillRevealed": True, "scenario": scenario["prompt"], "userPlan": user_plan, **result}
