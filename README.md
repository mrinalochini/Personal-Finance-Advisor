# Guided Wealth — Python Frontend

A Python/Streamlit frontend for the Personal Finance Advisor FastAPI backend.

## Features

- Login / signup
- Goal Milestone Hub
- Financial Diary
- Diary Insights
- Regret Mining
- Suggested Budgets
- Fire Drills
- Proxy Mode
- Transactions
- AI Coach

Automation Rules and Cash-Floor Guardrail are intentionally not included.

## Run

1. Make sure the FastAPI backend is running on port 3000.
2. Open PowerShell in this folder.
3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Start the frontend:

```powershell
python -m streamlit run app.py
```

The Streamlit frontend normally opens at:

http://localhost:8501

If the backend uses another URL:

```powershell
$env:API_BASE_URL="http://127.0.0.1:3000"
python -m streamlit run app.py
```
