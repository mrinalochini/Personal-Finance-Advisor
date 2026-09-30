from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Transaction
from auth import get_current_user
from llm_client import ask_gemini_for_json


router = APIRouter()


# ============================================================
# FIRE DRILL SCENARIOS
# ============================================================

SCENARIOS = {

    "rent_increase": {
        "id": "rent_increase",
        "prompt": (
            "Your landlord just told you rent is going up "
            "₹200 per month starting next month. "
            "Walk me through what you'd cut or change."
        ),
    },

    "medical_bill": {
        "id": "medical_bill",
        "prompt": (
            "You just got a surprise ₹350 medical bill "
            "due in two weeks. What's your plan to cover it?"
        ),
    },

}


# ============================================================
# DATABASE
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# GET SCENARIO
# ============================================================

@router.get("/firedrill/scenario/{scenario_id}")
def get_scenario(
    scenario_id: str
):

    scenario = SCENARIOS.get(
        scenario_id
    )

    if not scenario:

        raise HTTPException(
            404,
            "Unknown scenario."
        )

    return {
        "drill": True,
        **scenario
    }


# ============================================================
# RESPOND TO FIRE DRILL
# ============================================================

@router.post("/firedrill/respond")
def respond_to_drill(

    scenario_id: str,

    user_plan: str,

    user_id: int = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),
):

    scenario = SCENARIOS.get(
        scenario_id
    )

    if not scenario:

        raise HTTPException(
            404,
            "Unknown scenario."
        )


    # --------------------------------------------------------
    # GET USER TRANSACTIONS
    # --------------------------------------------------------

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id
        )
        .all()
    )


    spend_by_category = {}

    total_income = 0.0


    for transaction in transactions:

        if transaction.type == "expense":

            category = transaction.category

            spend_by_category[category] = (
                spend_by_category.get(
                    category,
                    0
                )
                + transaction.amount
            )

        elif transaction.type == "income":

            total_income += transaction.amount


    # --------------------------------------------------------
    # AI SCORING PROMPT
    # --------------------------------------------------------

    scoring_prompt = """
You are scoring whether a user's stated financial plan
would realistically cover a surprise expense, given
their real spending data.

Respond with ONLY a JSON object in this exact shape:

{
  "feasible_percent": <integer 0-100>,
  "verdict": <one short sentence, encouraging but honest>,
  "suggestion": <one short sentence with a concrete alternative if their plan falls short>
}

All monetary amounts must be expressed in Indian Rupees (₹).
Never use $, USD, or other currency symbols.
""".strip()


    # --------------------------------------------------------
    # USER CONTEXT
    # --------------------------------------------------------

    user_context = (

        f'Scenario: "{scenario["prompt"]}"\n'

        f'User\'s stated plan: "{user_plan}"\n'

        f"User's monthly income: ₹{total_income:.2f}\n"

        f"User's spending by category: "
        f"{spend_by_category}"

    )


    # --------------------------------------------------------
    # CALL AI
    # --------------------------------------------------------

    try:

        result = ask_gemini_for_json(
            scoring_prompt,
            user_context,
            max_tokens=300
        )

    except Exception as err:

        raise HTTPException(
            502,
            f"Couldn't reach the AI service: {err}"
        )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "drillRevealed": True,

        "scenario":
            scenario["prompt"],

        "userPlan":
            user_plan,

        **result

    }
