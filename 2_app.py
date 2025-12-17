import streamlit as st
import sqlite3
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Risk Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "CYBER/TECH" THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600&display=swap');

    /* GLOBAL RESET */
    .stApp {
        background-color: #0d1117; /* GitHub Dimmed */
        font-family: 'Inter', sans-serif;
    }
    
    /* TYPOGRAPHY */
    h1, h2, h3, .stMetricLabel {
        font-family: 'Fira Code', monospace !important;
        letter-spacing: -0.5px;
    }
    
    h1 {
        background: linear-gradient(90deg, #58a6ff, #7ee787);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
    }
    
    p, .stMarkdown {
        color: #8b949e !important;
    }

    /* CUSTOM CARDS */
    div.css-1r6slb0, div.stMarkdown { 
        /* Tweak default container behavior if needed */
    }

    .tech-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .tech-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }
    .tech-card h4 {
        color: #58a6ff;
        margin-top: 0;
        font-size: 1.1rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    /* METRICS */
    .metric-container {
        text-align: center;
        padding: 10px;
    }
    .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #e6edf3;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* INPUT FIELDS - DARK MODE */
    .stTextInput input, .stNumberInput input {
        background-color: #010409 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        font-family: 'Fira Code', monospace !important;
        border-radius: 6px;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 1px #58a6ff !important;
    }

    /* BUTTONS */
    .stButton button {
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        border: none;
        font-family: 'Fira Code', monospace;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #2ea043, #3fb950);
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.4);
        border: none;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* DATAFRAME */
    .stDataFrame {
        border: 1px solid #30363d;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. LOGIC ---
def calculate_score(income, debt, years_employed, history_pct):
    score = 0
    # DTI Logic
    if income == 0: dti = 100 
    else: dti = (debt / income)
    
    if dti < 0.2: score += 40
    elif dti < 0.4: score += 30
    elif dti < 0.6: score += 10
    else: score += 0
    
    # Stability Logic
    if years_employed >= 5: score += 30
    elif years_employed >= 2: score += 20
    else: score += 10
    
    # History Logic
    if history_pct >= 0.95: score += 30
    elif history_pct >= 0.85: score += 20
    elif history_pct >= 0.70: score += 10
    else: score += 0
    
    return score, dti

def get_decision(score):
    if score >= 80:
        return "APPROVED", "3.5% (Prime)", "#2ea043", "✅" 
    elif score >= 50:
        return "APPROVED", "8.0% (Sub-Prime)", "#d2a8ff", "⚠️"
    else:
        return "REJECTED", "N/A", "#ff7b72", "🚫"

# --- 2. LAYOUT ---
st.title("⚡ Credit_Risk_Engine")
st.markdown("`v1.0.4` | Automated decisioning powered by **Python** & **SQL**.")
st.write("")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to:", ["Loan Simulator", "Admin Database"])
    st.write("---")
    st.caption("System Status: ● Online")

if page == "Loan Simulator":
    # 2-Column Inputs wrapped in HTML Cards for styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tech-card"><h4>👤 Applicant Financials</h4>', unsafe_allow_html=True)
        income = st.number_input("Monthly Income ($)", value=10000, step=500)
        debt = st.number_input("Total Debt ($)", value=2000, step=500)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="tech-card"><h4>📜 History & Stability</h4>', unsafe_allow_html=True)
        years = st.number_input("Years Employed", value=3, step=1)
        history = st.slider("Repayment Score (%)", 0, 100, 95) / 100.0
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    
    # Full Width Action Button
    if st.button(">> EXECUTE_RISK_ALGORITHM()"):
        final_score, dti = calculate_score(income, debt, years, history)
        decision, interest, color, icon = get_decision(final_score)
        
        # Spacer
        st.write("")
        st.write("")

        # --- RESULT BANNER ---
        st.markdown(f"""
        <div style="background-color: {color}15; border: 1px solid {color}; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 30px;">
            <div style="font-family: 'Fira Code'; font-size: 1.2rem; color: {color}; margin-bottom: 10px;">ALGORITHM OUTPUT</div>
            <h1 style="color: {color}; margin: 0; background: none; -webkit-text-fill-color: {color}; font-size: 4rem !important;">{icon} {decision}</h1>
            <p style="color: #c9d1d9 !important; font-size: 1.2rem; margin-top: 10px;">Interest Rate: <strong style="color: white;">{interest}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- METRICS GRID ---
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class="tech-card metric-container">
                <div class="metric-label">Risk Score</div>
                <div class="metric-value" style="color: {color};">{final_score}/100</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="tech-card metric-container">
                <div class="metric-label">DTI Ratio</div>
                <div class="metric-value">{int(dti * 100)}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
            <div class="tech-card metric-container">
                <div class="metric-label">Data Points</div>
                <div class="metric-value">3</div>
            </div>
            """, unsafe_allow_html=True)

        # Logic Trace
        with st.expander("View Logic Trace"):
            st.code(f"""
[LOG] Processing Application...
> DTI Calculated: {dti:.2f} ({int(dti*100)}%) -> Score Impact: {40 if dti < 0.2 else (30 if dti < 0.4 else 0)} pts
> Stability: {years} Years -> Score Impact: {30 if years >= 5 else 10} pts
> History: {int(history*100)}% -> Score Impact: {30 if history >= 0.95 else 20} pts
--------------------------------------------------
TOTAL SCORE: {final_score}/100
DECISION: {decision}
            """, language="json")

elif page == "Admin Database":
    st.title("📂 SQL Database")
    
    conn = sqlite3.connect('credit_risk.db')
    query = """
    SELECT 
        a.id, 
        a.name, 
        a.monthly_income, 
        c.total_debt, 
        l.repayment_on_time_pct
    FROM applicants a
    JOIN credit_bureau c ON a.id = c.applicant_id
    JOIN loan_history l ON a.id = l.applicant_id
    LIMIT 10
    """
    df = pd.read_sql_query(query, conn)
    
    st.dataframe(df, use_container_width=True)
    st.caption("Connected to: sqlite:///credit_risk.db")
    
    st.markdown("### Raw Query Execution")
    st.code(query, language="sql")
    conn.close()
