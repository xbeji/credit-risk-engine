import streamlit as st
import sqlite3
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Risk Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "TECH / GITHUB DARK" THEME ---
st.markdown("""
<style>
    /* 1. Main Background */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* 2. Typography */
    h1, h2, h3, h4, h5, h6, .stMetricLabel, .stMarkdown {
        font-family: 'Source Code Pro', 'Courier New', monospace !important;
    }
    h1 {
        background: -webkit-linear-gradient(90deg, #58a6ff, #7ee787);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* 3. Inputs & Widgets */
    .stTextInput input, .stNumberInput input {
        background-color: #010409 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #010409 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }
    
    /* 4. Custom Cards */
    .tech-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .tech-card:hover {
        border-color: #58a6ff;
    }
    
    /* 5. Metrics styling */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b949e;
    }
    
    /* 6. Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. BUSINESS ANALYTICS LOGIC ---
def calculate_score(income, debt, years_employed, history_pct):
    score = 0
    
    # Factor 1: DTI (40%)
    if income == 0: dti = 100 
    else: dti = (debt / income)
    
    if dti < 0.2: score += 40
    elif dti < 0.4: score += 30
    elif dti < 0.6: score += 10
    else: score += 0
    
    # Factor 2: Stability (30%)
    if years_employed >= 5: score += 30
    elif years_employed >= 2: score += 20
    else: score += 10
    
    # Factor 3: History (30%)
    if history_pct >= 0.95: score += 30
    elif history_pct >= 0.85: score += 20
    elif history_pct >= 0.70: score += 10
    else: score += 0
    
    return score, dti

def get_decision(score):
    if score >= 80:
        return "APPROVED", "3.5% (Prime)", "#7ee787" # Green
    elif score >= 50:
        return "APPROVED", "8.0% (Sub-Prime)", "#d2a8ff" # Purple
    else:
        return "REJECTED", "N/A", "#ff7b72" # Red

# --- 2. UI LAYOUT ---
st.title("💻 Credit_Risk_Engine.py")
st.markdown("Automated decisioning powered by **Python** & **SQL**.")
st.write("---")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Loan Simulator", "Admin Database"])

if page == "Loan Simulator":
    # 2-Column Layout for Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tech-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Applicant Financials")
        income = st.number_input("Monthly Income ($)", value=10000, step=500)
        debt = st.number_input("Total Debt ($)", value=2000, step=500)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tech-card">', unsafe_allow_html=True)
        st.markdown("#### 📜 History & Stability")
        years = st.number_input("Years Employed", value=3, step=1)
        history = st.slider("Repayment Score (%)", 0, 100, 95) / 100.0
        st.markdown('</div>', unsafe_allow_html=True)

    # Action Button
    if st.button("RUN_ALGORITHM()", type="primary"):
        final_score, dti = calculate_score(income, debt, years, history)
        decision, interest, color = get_decision(final_score)
        
        # --- RESULTS DASHBOARD ---
        st.write("---")
        st.subheader(">> Algorithm Output")
        
        # Row 1: The Decision Banner
        st.markdown(f"""
        <div style="background-color: {color}20; border: 1px solid {color}; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h2 style="color: {color}; margin:0;">DECISION: {decision}</h2>
            <p style="color: #c9d1d9; margin:0;">Interest Rate: <strong>{interest}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Row 2: Metrics Cards
        m1, m2, m3 = st.columns(3)
        
        with m1:
            st.markdown(f"""
            <div class="tech-card" style="text-align: center;">
                <div class="metric-label">RISK SCORE</div>
                <div class="metric-value">{final_score}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="tech-card" style="text-align: center;">
                <div class="metric-label">DTI RATIO</div>
                <div class="metric-value">{int(dti * 100)}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="tech-card" style="text-align: center;">
                <div class="metric-label">DATA POINTS</div>
                <div class="metric-value">3</div>
            </div>
            """, unsafe_allow_html=True)

        # Logic Breakdown
        with st.expander("Show Logic Trace"):
            st.code(f"""
# Calculation Trace
def risk_logic():
    dti_score = {40 if dti < 0.2 else (30 if dti < 0.4 else 0)}  # Based on {int(dti*100)}%
    stability_score = {30 if years >= 5 else 10}  # Based on {years} years
    history_score = {30 if history >= 0.95 else 20}  # Based on {int(history*100)}%
    
    total = {final_score}
    return "{decision}"
            """, language="python")

elif page == "Admin Database":
    st.header("📂 SQL Database View")
    
    conn = sqlite3.connect('credit_risk.db')
    query = """
    SELECT a.name, a.monthly_income, c.total_debt, l.repayment_on_time_pct
    FROM applicants a
    JOIN credit_bureau c ON a.id = c.applicant_id
    JOIN loan_history l ON a.id = l.applicant_id
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    
    # Custom Table Styling
    st.dataframe(df, use_container_width=True)
    st.caption("Connected to: sqlite:///credit_risk.db")
    
    with st.expander("View Raw SQL Query"):
        st.code(query, language="sql")
    
    conn.close()
