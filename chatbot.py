from sqlalchemy.orm import Session
from models import Transaction
from llm_client import ask_gemini_with_tools

SYSTEM_PROMPT = """
You are a friendly, practical personal finance advisor chatbot.

Use the get_spending_by_category tool to retrieve the user's real financial numbers.
Never guess, invent, or estimate financial amounts.

IMPORTANT CURRENCY RULE:
All financial amounts in the user's account are in Indian Rupees (INR).
Always display INR amounts using the ₹ symbol.
For example, if the tool returns totalSpent = 1500, write ₹1,500.
NEVER use $, USD, or any other currency symbol unless the user explicitly asks
to convert the amount to another currency.

Keep answers short (2-4 sentences) and conversational.
You are not a licensed financial advisor; keep guidance general and encourage
professional advice for major financial decisions.
""".strip()

TOOLS = [
    {
        "name": "get_spending_by_category",
        "description": "Returns the user's total spending in a given category.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {"type": "STRING", "description": "e.g. 'food', 'shopping', 'entertainment'"},
            },
            "required": ["category"],
        },
    }
]


def make_tool_executor(db: Session, user_id: int):
    """Bound to this request's authenticated user_id, so Gemini can never query someone else's data."""

    def tool_executor(tool_name: str, tool_args: dict) -> dict:
        if tool_name != "get_spending_by_category":
            return {"error": f"Unknown tool: {tool_name}"}

        total = sum(
            t.amount
            for t in db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.category == tool_args["category"],
                Transaction.type == "expense",
            )
            .all()
        )
        return {"category": tool_args["category"], "totalSpent": round(total, 2)}

    return tool_executor


def ask_finance_bot(question: str, db: Session, user_id: int) -> str:
    return ask_gemini_with_tools(
        system_prompt=SYSTEM_PROMPT,
        user_message=question,
        tools=TOOLS,
        tool_executor=make_tool_executor(db, user_id),
    )
