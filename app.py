import os
import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:3000"
)


st.set_page_config(
    page_title="Guided Wealth",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME
# ============================================================

st.markdown(
    """
    <style>

    /* =========================================================
       GUIDED WEALTH — MODERN COLORFUL THEME
       ========================================================= */

    /* ---------- Main Application ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.18), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(14, 165, 233, 0.16), transparent 25%),
            radial-gradient(circle at 80% 90%, rgba(236, 72, 153, 0.12), transparent 30%),
            linear-gradient(135deg, #080b1a 0%, #10152f 45%, #0b1024 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- Typography ---------- */

    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #f8fafc !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    p, label, .stMarkdown {
        color: #cbd5e1;
    }

    .small {
        color: #94a3b8;
        font-size: 0.9rem;
    }

    /* ---------- Glass Cards ---------- */

    .card {
        background: linear-gradient(
            145deg,
            rgba(30, 41, 78, 0.88),
            rgba(15, 23, 52, 0.82)
        );
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(14px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow:
            0 20px 45px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(124, 58, 237, 0.12);
    }

    /* ---------- Metric Cards ---------- */

    .metric-card {
        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.22),
                rgba(37, 99, 235, 0.15)
            );
        border: 1px solid rgba(167, 139, 250, 0.28);
        border-radius: 22px;
        padding: 24px;
        text-align: center;
        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
    }

    .metric-card h3 {
        font-size: 2rem;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #a78bfa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ---------- AI Coach ---------- */

    .coach {
        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.22),
                rgba(14, 165, 233, 0.16)
            );
        border-left: 5px solid #8b5cf6;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 12px 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    /* ---------- Badges ---------- */

    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        padding: 6px 13px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.25);
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(167, 139, 250, 0.25);
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1rem;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #a78bfa;
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(124, 58, 237, 0.35);
    }

    /* ---------- Inputs ---------- */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.75) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(148, 163, 184, 0.25) !important;
        border-radius: 12px !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 1px #8b5cf6 !important;
    }

    /* ---------- Select Boxes ---------- */

    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        border-color: rgba(148, 163, 184, 0.25);
        color: white;
    }

    /* ---------- Progress Bars ---------- */

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #7c3aed, #2563eb, #06b6d4);
        border-radius: 999px;
    }

    .stProgress > div > div {
        background: rgba(148, 163, 184, 0.15);
        border-radius: 999px;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background:
            radial-gradient(
                circle at 20% 10%,
                rgba(124, 58, 237, 0.22),
                transparent 30%
            ),
            linear-gradient(180deg, #0b1024 0%, #080b18 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: rgba(30, 41, 78, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.12);
        box-shadow: none;
        text-align: left;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(
            90deg,
            rgba(124, 58, 237, 0.55),
            rgba(37, 99, 235, 0.45)
        );
        border-color: rgba(167, 139, 250, 0.35);
    }

    /* ---------- Tabs ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.55);
        padding: 7px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        padding: 8px 18px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: white !important;
    }

    /* ---------- Expanders ---------- */

    .streamlit-expanderHeader {
        background: rgba(30, 41, 78, 0.65);
        border-radius: 14px;
        color: #f8fafc !important;
        font-weight: 700;
    }

    /* ---------- Alerts / Info Boxes ---------- */

    [data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.15);
    }

    /* ---------- Chat ---------- */

    [data-testid="stChatMessage"] {
        background: rgba(30, 41, 78, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        margin-bottom: 10px;
    }

    /* ---------- Dividers ---------- */

    hr {
        border-color: rgba(148, 163, 184, 0.12) !important;
    }

    /* ---------- Scrollbar ---------- */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080b18;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#7c3aed, #2563eb);
        border-radius: 10px;
    }

    /* ---------- Selection ---------- */

    ::selection {
        background: rgba(139, 92, 246, 0.45);
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def headers():
    token = st.session_state.get("token")

    if token:
        return {
            "Authorization": f"Bearer {token}"
        }

    return {}


def api_get(path, params=None):
    return requests.get(
        API_BASE + path,
        headers=headers(),
        params=params,
        timeout=60,
    )


def api_post(path, params=None):
    return requests.post(
        API_BASE + path,
        headers=headers(),
        params=params,
        timeout=60,
    )


def handle_response(response):
    """
    Handles backend responses safely.

    Returns:
        JSON data when successful.
        None when an error occurs.
    """

    if response.ok:
        try:
            return response.json()
        except Exception:
            return {}

    try:
        error_data = response.json()
        detail = error_data.get(
            "detail",
            response.text
        )
    except Exception:
        detail = response.text

    st.error(
        f"Backend error ({response.status_code}): {detail}"
    )

    return None


# ============================================================
# SESSION STATE
# ============================================================

if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "Goal Hub"

if "selected_drill" not in st.session_state:
    st.session_state.selected_drill = "rent_increase"


# ============================================================
# LOGIN / SIGNUP
# ============================================================

def auth_page():

    st.markdown("# 💰 Guided Wealth")

    st.markdown(
        "### Warm, milestone-driven financial guidance"
    )

    st.write(
        "Connect to your Personal Finance Advisor backend."
    )

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Create account"
        ]
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    with tab1:

        with st.form("login"):

            email = st.text_input(
                "Email"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if submitted:

            if not email or not password:

                st.warning(
                    "Please enter both email and password."
                )

            else:

                try:

                    response = requests.post(
                        API_BASE + "/login",
                        params={
                            "email": email,
                            "password": password
                        },
                        timeout=30
                    )

                    data = handle_response(response)

                    if data:

                        token = data.get("token")

                        if token:

                            st.session_state.token = token

                            st.success(
                                "Login successful."
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Login succeeded, but no authentication token was returned."
                            )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to backend: {e}"
                    )

    # --------------------------------------------------------
    # SIGNUP
    # --------------------------------------------------------

    with tab2:

        with st.form("signup"):

            email = st.text_input(
                "Email",
                key="signup_email"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            submitted = st.form_submit_button(
                "Create account",
                use_container_width=True
            )

        if submitted:

            if not email or not password:

                st.warning(
                    "Please enter both email and password."
                )

            else:

                try:

                    response = requests.post(
                        API_BASE + "/signup",
                        params={
                            "email": email,
                            "password": password
                        },
                        timeout=30
                    )

                    data = handle_response(response)

                    if data:

                        st.success(
                            "Account created successfully. "
                            "You can now log in."
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to backend: {e}"
                    )


# ============================================================
# SHOW AUTH PAGE IF NOT LOGGED IN
# ============================================================

if not st.session_state.token:

    auth_page()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "Guided Wealth"
)

st.sidebar.caption(
    "Your financial companion"
)


pages = [
    "Goal Hub",
    "Financial Diary",
    "Regret Mining",
    "Suggested Budgets",
    "Fire Drills",
    "Proxy Mode",
    "Transactions",
    "AI Coach",
]


for page in pages:

    if st.sidebar.button(
        page,
        use_container_width=True
    ):

        st.session_state.page = page


st.sidebar.divider()

st.sidebar.caption(
    f"Backend: {API_BASE}"
)


if st.sidebar.button(
    "Log out",
    use_container_width=True
):

    st.session_state.token = None

    st.rerun()


# ============================================================
# GOAL HUB
# ============================================================

def goal_hub():

    st.title(
        "Good to see you again 🌤️"
    )

    st.write(
        "Let's take a calm look at where your money "
        "is going and where you're headed."
    )


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    dashboard = handle_response(
        api_get("/dashboard")
    )

    if not dashboard:
        return


    income = float(
        dashboard.get(
            "total_income",
            0
        )
    )

    expense = float(
        dashboard.get(
            "total_expense",
            0
        )
    )

    buffer = income - expense


    if income > 0:

        health = max(
            0,
            min(
                100,
                round(
                    (buffer / income) * 100
                )
            )
        )

    else:

        health = 0


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>₹{income:,.0f}</h3>
                <div class="small">
                    Total income
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>₹{expense:,.0f}</h3>
                <div class="small">
                    Total expenses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <h3>₹{buffer:,.0f}</h3>
                <div class="small">
                    Current buffer
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # RUNWAY HEALTH
    # --------------------------------------------------------

    st.markdown(
        "## Runway health"
    )

    st.progress(
        health / 100
    )

    st.write(
        f"**{health}% buffer health** — "
        "income remaining after recorded expenses."
    )


    # --------------------------------------------------------
    # GOALS
    # --------------------------------------------------------

    st.markdown(
        "## Milestone goals"
    )


    goals = [

        (
            "🏠",
            "House Down Payment",
            "Build toward your home fund",
            62
        ),

        (
            "🔥",
            "FIRE Target",
            "Grow toward long-term financial independence",
            34
        ),

        (
            "🛟",
            "Emergency Vault",
            "Create a stronger safety reserve",
            78
        )

    ]


    cols = st.columns(3)


    for col, (
        icon,
        name,
        desc,
        progress
    ) in zip(cols, goals):

        with col:

            st.markdown(
                f"""
                <div class="card">
                    <h2>{icon}</h2>
                    <h3>{name}</h3>
                    <p>{desc}</p>
                    <div class="small">
                        {progress}% progress
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                progress / 100
            )


    # --------------------------------------------------------
    # AI COACH SWEEP
    # --------------------------------------------------------

    st.markdown(
        "## AI coach sweep"
    )


    question = st.text_input(
        "Ask for a quick financial check-in",
        placeholder=(
            "e.g. What should I watch this month?"
        ),
        key="coach_sweep"
    )


    if st.button(
        "Run coach sweep",
        use_container_width=True
    ) and question:

        data = handle_response(
            api_post(
                "/chat",
                {
                    "question": question
                }
            )
        )

        if data:

            st.markdown(
                f"""
                <div class="coach">
                    {data.get("answer", "")}
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # QUICK SCENARIOS
    # --------------------------------------------------------

    st.markdown(
        "## Quick scenario tests"
    )


    cols = st.columns(2)


    scenarios = [

        (
            "rent_increase",
            "🏠 Rent increase"
        ),

        (
            "medical_bill",
            "🩺 Surprise medical bill"
        )

    ]


    for col, (
        scenario_id,
        label
    ) in zip(cols, scenarios):

        with col:

            if st.button(
                label,
                use_container_width=True
            ):

                st.session_state.selected_drill = scenario_id

                st.session_state.page = "Fire Drills"

                st.rerun()


# ============================================================
# FINANCIAL DIARY
# ============================================================

def financial_diary():

    st.title(
        "📔 Financial Diary"
    )

    st.write(
        "Write what happened in your own words. "
        "The AI will turn it into structured "
        "transaction information for you to review."
    )


    # --------------------------------------------------------
    # DIARY ENTRY
    # --------------------------------------------------------

    with st.form(
        "diary_form"
    ):

        note = st.text_area(
            "What happened?",
            placeholder=(
                "I spent ₹850 at a restaurant "
                "after a stressful day..."
            ),
            height=130
        )


        submitted = st.form_submit_button(
            "Analyze diary entry",
            use_container_width=True
        )


    if submitted and note:

        data = handle_response(
            api_post(
                "/diary/parse",
                {
                    "note": note
                }
            )
        )


        if data:

            parsed = data.get(
                "parsed",
                {}
            )

            st.session_state.diary_note = note

            st.session_state.diary_parsed = parsed


    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    if "diary_parsed" in st.session_state:

        parsed = st.session_state.diary_parsed


        st.markdown(
            "## Review before saving"
        )


        with st.form(
            "diary_confirm"
        ):

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(
                    parsed.get(
                        "amount",
                        0
                    )
                )
            )


            category = st.text_input(
                "Category",
                value=str(
                    parsed.get(
                        "category",
                        "other"
                    )
                )
            )


            merchant = st.text_input(
                "Merchant",
                value=str(
                    parsed.get(
                        "merchant",
                        "unknown"
                    )
                )
            )


            mood = st.text_input(
                "Mood",
                value=str(
                    parsed.get(
                        "mood",
                        "neutral"
                    )
                )
            )


            save = st.form_submit_button(
                "Confirm & save",
                use_container_width=True
            )


        if save:

            params = {

                "amount": amount,

                "category": category,

                "mood": mood,

                "merchant": merchant,

                "note": st.session_state.get(
                    "diary_note",
                    ""
                )

            }


            data = handle_response(
                api_post(
                    "/diary/confirm",
                    params
                )
            )


            if data:

                st.success(
                    "Diary entry saved as a transaction."
                )

                st.session_state.pop(
                    "diary_parsed",
                    None
                )


    # --------------------------------------------------------
    # INSIGHT
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        "## Diary insight"
    )


    if st.button(
        "Find my spending pattern",
        use_container_width=True
    ):

        data = handle_response(
            api_get(
                "/diary/insight"
            )
        )


        if data:

            st.markdown(
                f"""
                <div class="coach">
                    {data.get("insight", "")}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# REGRET MINING
# ============================================================

def regret_mining():

    st.title(
        "🔎 Regret Mining"
    )

    st.write(
        "Look back at recent expenses and identify "
        "purchases you would handle differently."
    )


    data = handle_response(
        api_get(
            "/regret/retro",
            {
                "limit": 20
            }
        )
    )


    if not data:
        return


    transactions_data = data.get(
        "transactions",
        []
    )


    if not transactions_data:

        st.info(
            "No expense history found yet."
        )

        return


    # --------------------------------------------------------
    # TRANSACTIONS
    # --------------------------------------------------------

    for transaction in transactions_data:

        left, middle, right = st.columns(
            [3, 2, 1]
        )


        with left:

            st.markdown(
                f"**{transaction.get('merchant') or 'Unknown merchant'}**"
            )

            st.caption(
                f"{transaction.get('category', 'other')} · "
                f"{transaction.get('date', '')}"
            )


        with middle:

            st.write(
                f"₹{float(transaction.get('amount', 0)):,.2f}"
            )


        with right:

            if st.button(
                "Regret",
                key=f"regret_{transaction['id']}"
            ):

                result = handle_response(
                    api_post(
                        "/regret/tag",
                        {
                            "transaction_id":
                                transaction["id"],

                            "regret":
                                True
                        }
                    )
                )


                if result:

                    st.success(
                        "Tagged."
                    )

                    st.rerun()


    # --------------------------------------------------------
    # SUGGESTED BUDGETS
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        "## What your history suggests"
    )


    if st.button(
        "Generate suggested budgets",
        use_container_width=True
    ):

        data = handle_response(
            api_get(
                "/regret/suggested-budgets"
            )
        )


        if data:

            suggestions = data.get(
                "suggestions",
                []
            )


            if not suggestions:

                st.info(
                    data.get(
                        "message",
                        "No suggestions yet."
                    )
                )


            for suggestion in suggestions:

                category = suggestion.get(
                    "category",
                    "other"
                )


                suggested_limit = float(
                    suggestion.get(
                        "suggestedLimit",
                        0
                    )
                )


                phrasing = suggestion.get(
                    "phrasing",
                    ""
                )


                st.markdown(
                    f"""
                    <div class="card">

                        <span class="badge">
                            {category}
                        </span>

                        <h3>
                            ₹{suggested_limit:,.0f}
                            / month
                        </h3>

                        <p>
                            {phrasing}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# SUGGESTED BUDGETS
# ============================================================

def suggested_budgets():

    st.title(
        "🎯 Suggested Budgets"
    )

    st.write(
        "Turn patterns from your spending history "
        "into practical monthly limits."
    )


    data = handle_response(
        api_get(
            "/regret/suggested-budgets"
        )
    )


    if not data:
        return


    suggestions = data.get(
        "suggestions",
        []
    )


    if not suggestions:

        st.info(
            data.get(
                "message",
                "Tag some regretted purchases first."
            )
        )

        return


    # --------------------------------------------------------
    # EACH SUGGESTION
    # --------------------------------------------------------

    for i, suggestion in enumerate(
        suggestions
    ):

        category = suggestion.get(
            "category",
            "other"
        )


        suggested = float(
            suggestion.get(
                "suggestedLimit",
                0
            )
        )


        phrasing = suggestion.get(
            "phrasing",
            ""
        )


        st.markdown(
            f"### {category.title()}"
        )


        if phrasing:

            st.write(
                phrasing
            )


        col1, col2 = st.columns(
            [2, 1]
        )


        with col1:

            limit = st.number_input(
                "Monthly limit",
                min_value=0.0,
                value=suggested,
                key=f"budget_{i}"
            )


        with col2:

            if st.button(
                "Save budget",
                key=f"save_budget_{i}",
                use_container_width=True
            ):

                result = handle_response(
                    api_post(
                        "/budgets",
                        {
                            "category": category,

                            "limit_amount": limit
                        }
                    )
                )


                if result:

                    st.success(
                        "Budget saved."
                    )


        # ----------------------------------------------------
        # BUDGET STATUS
        # ----------------------------------------------------

        status = handle_response(
            api_get(
                f"/budgets/status/{category}"
            )
        )


        if status and "spent" in status:

            spent = float(
                status.get(
                    "spent",
                    0
                )
            )


            limit_value = float(
                status.get(
                    "limit",
                    0
                )
            )


            if limit_value > 0:

                progress = min(
                    1,
                    spent / limit_value
                )

            else:

                progress = 0


            st.progress(
                progress
            )


            st.caption(
                f"Spent ₹{spent:,.0f} "
                f"of ₹{limit_value:,.0f}"
            )


# ============================================================
# FIRE DRILLS
# ============================================================

def fire_drills():

    st.title(
        "🚨 Fire Drills"
    )

    st.write(
        "Practice responding to a surprise financial "
        "event before one happens."
    )


    scenario_options = {

        "rent_increase":
            "🏠 Rent increase",

        "medical_bill":
            "🩺 Surprise medical bill"

    }


    default = st.session_state.get(
        "selected_drill",
        "rent_increase"
    )


    selected = st.selectbox(
        "Choose a scenario",

        list(
            scenario_options.keys()
        ),

        index=list(
            scenario_options.keys()
        ).index(default),

        format_func=lambda x:
            scenario_options[x]
    )


    # --------------------------------------------------------
    # SCENARIO
    # --------------------------------------------------------

    scenario = handle_response(
        api_get(
            f"/firedrill/scenario/{selected}"
        )
    )


    if scenario:
        st.markdown("### Scenario")
        st.info(scenario.get("prompt", ""))


        # ----------------------------------------------------
        # PLAN
        # ----------------------------------------------------

        with st.form(
            "fire_drill_form"
        ):

            plan = st.text_area(
                "What's your plan?",

                placeholder=(
                    "I would reduce dining out, "
                    "pause a purchase, and use part "
                    "of my savings..."
                ),

                height=150
            )


            submit = st.form_submit_button(
                "Test my plan",
                use_container_width=True
            )


        if submit and plan:

            result = handle_response(
                api_post(
                    "/firedrill/respond",
                    {
                        "scenario_id":
                            selected,

                        "user_plan":
                            plan
                    }
                )
            )


            if result:

                st.markdown(
                    "## Drill result"
                )


                percent = int(
                    result.get(
                        "feasible_percent",
                        0
                    )
                )


                percent = max(
                    0,
                    min(
                        100,
                        percent
                    )
                )


                st.metric(
                    "Estimated gap covered",
                    f"{percent}%"
                )


                st.progress(
                    percent / 100
                )


                st.markdown(
                    f"""
                    <div class="coach">
                        {result.get("verdict", "")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.info(
                    result.get(
                        "suggestion",
                        ""
                    )
                )


# ============================================================
# PROXY MODE
# ============================================================

def proxy_mode():

    st.title(
        "💬 Proxy Mode"
    )

    st.write(
        "Create a calm, judgment-free financial "
        "message. Nothing is sent automatically."
    )


    recipient = st.selectbox(
        "Who is this message for?",

        [
            "partner",
            "roommate",
            "parent",
            "friend",
            "family member"
        ]
    )


    if st.button(
        "Draft message",
        use_container_width=True
    ):

        data = handle_response(
            api_post(
                "/proxy/draft",
                {
                    "recipient_label":
                        recipient
                }
            )
        )


        if data:

            st.session_state.proxy_draft = (
                data.get(
                    "draft",
                    ""
                )
            )


    # --------------------------------------------------------
    # DRAFT
    # --------------------------------------------------------

    if "proxy_draft" in st.session_state:

        draft = st.text_area(
            "Editable draft",

            value=st.session_state.proxy_draft,

            height=180
        )


        st.session_state.proxy_draft = draft


        st.info(
            "This is only a draft. Guided Wealth "
            "never automatically sends it."
        )


        if st.button(
            "Copy-ready preview",
            use_container_width=True
        ):

            st.code(
                draft
            )


# ============================================================
# TRANSACTIONS
# ============================================================

def transactions():

    st.title(
        "💳 Transactions"
    )


    # --------------------------------------------------------
    # ADD TRANSACTION
    # --------------------------------------------------------

    with st.expander(
        "Add transaction"
    ):

        with st.form(
            "transaction_form"
        ):

            amount = st.number_input(
                "Amount",
                min_value=0.0
            )


            category = st.text_input(
                "Category",
                placeholder="food"
            )


            tx_type = st.selectbox(
                "Type",
                [
                    "expense",
                    "income"
                ]
            )


            merchant = st.text_input(
                "Merchant"
            )


            submit = st.form_submit_button(
                "Add transaction"
            )


        if submit:

            if not category:

                st.warning(
                    "Please enter a category."
                )

            else:

                result = handle_response(
                    api_post(
                        "/transactions",
                        {
                            "amount":
                                amount,

                            "category":
                                category,

                            "type":
                                tx_type,

                            "merchant":
                                merchant or None
                        }
                    )
                )


                if result:

                    st.success(
                        "Transaction added."
                    )


    # --------------------------------------------------------
    # TRANSACTION LIST
    # --------------------------------------------------------

    data = handle_response(
        api_get(
            "/transactions"
        )
    )


    if data:

        st.markdown(
            "## Recorded transactions"
        )


        for transaction in reversed(data):

            sign = (
                "+"
                if transaction["type"] == "income"
                else "-"
            )


            st.write(
                f"**{sign}₹"
                f"{float(transaction['amount']):,.2f}** · "
                f"{transaction['category']} · "
                f"{transaction.get('merchant') or 'Unknown'}"
            )


# ============================================================
# AI COACH
# ============================================================

def ai_coach():

    st.title(
        "🤖 AI Coach"
    )

    st.write(
        "Ask questions about your real recorded spending."
    )


    question = st.chat_input(
        "Ask something like: How much did I spend on food?"
    )


    if question:

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )


        data = handle_response(
            api_post(
                "/chat",
                {
                    "question":
                        question
                }
            )
        )


        if data:

            with st.chat_message(
                "assistant"
            ):

                st.write(
                    data.get(
                        "answer",
                        ""
                    )
                )


# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.page


if page == "Goal Hub":

    goal_hub()


elif page == "Financial Diary":

    financial_diary()


elif page == "Regret Mining":

    regret_mining()


elif page == "Suggested Budgets":

    suggested_budgets()


elif page == "Fire Drills":

    fire_drills()


elif page == "Proxy Mode":

    proxy_mode()


elif page == "Transactions":

    transactions()


elif page == "AI Coach":

    ai_coach()
