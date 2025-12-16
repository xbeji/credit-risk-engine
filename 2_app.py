import streamlit as st
import sqlite3
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Credit Risk Engine", page_icon="🏦")
st.title("🏦 Dynamic Credit Risk Scoring Engine")

# --- 1. THE BUSINESS ANALYTICS LAYER (Logic) ---
def calculate_score(income, debt, years_employed, history_pct):
    """
    Calculates a credit score (0-100) based on weighted financial factors.
    """
    score = 0
    
    # Factor 1: Debt-to-Income Ratio (DTI) - Weight: 40%
    # Lower DTI is better. If Debt > Income, it's bad.
    if income == 0: dti = 100 
    else: dti = (debt / income)
    
    if dti < 0.2: score += 40      # Excellent
    elif dti < 0.4: score += 30    # Good
    elif dti < 0.6: score += 10    # Risky
    else: score += 0               # Dangerous
    
    # Factor 2: Employment Stability - Weight: 30%
    if years_employed >= 5: score += 30
    elif years_employed >= 2: score += 20
    else: score += 10
    
    # Factor 3: Repayment History - Weight: 30%
    # Assuming history_pct is between 0.0 and 1.0
    if history_pct >= 0.95: score += 30
    elif history_pct >= 0.85: score += 20
    elif history_pct >= 0.70: score += 10
    else: score += 0
    
    return score

def get_decision(score):
    if score >= 80:
        return "APPROVED", "3.5% (Prime)", "success"
    elif score >= 50:
        return "APPROVED", "8.0% (Sub-Prime)", "warning"
    else:
        return "REJECTED", "N/A", "error"

# --- 2. THE INFORMATION SYSTEMS LAYER (Database View) ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Loan Simulator", "Admin Dashboard"])

if page == "Admin Dashboard":
    st.header("📂 Bank Database View")
    st.markdown("This view queries the SQLite database directly.")
    
    # Connect to DB
    conn = sqlite3.connect('credit_risk.db')
    
    # Complex SQL JOIN to show mastery of Relational Data
    sql_query = """
    SELECT 
        a.name, 
        a.monthly_income, 
        c.total_debt, 
        l.repayment_on_time_pct,
        (c.total_debt / a.monthly_income) as DTI_Ratio
    FROM applicants a
    JOIN credit_bureau c ON a.id = c.applicant_id
    JOIN loan_history l ON a.id = l.applicant_id
    LIMIT 20
    """
    
    df = pd.read_sql_query(sql_query, conn)
    st.dataframe(df)
    st.caption("Displaying top 20 records with calculated DTI Ratios via SQL.")
    conn.close()

elif page == "Loan Simulator":
    st.header("💳 New Application Simulator")
    st.write("Enter applicant details to calculate real-time Risk Score.")
    
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Monthly Income (SAR)", value=10000, step=500)
        debt = st.number_input("Total Existing Debt (SAR)", value=2000, step=500)
    with col2:
        years = st.number_input("Years Employed", value=3, step=1)
        history = st.slider("Past Repayment Score (%)", 0, 100, 95) / 100.0

    if st.button("Calculate Risk Score"):
        # Run the Algorithm
        final_score = calculate_score(income, debt, years, history)
        decision, interest, status = get_decision(final_score)
        
        # Display Results
        st.divider()
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.metric(label="Credit Score", value=f"{final_score}/100")
        
        with col_res2:
            if status == "success":
                st.success(f"DECISION: {decision}")
            elif status == "warning":
                st.warning(f"DECISION: {decision}")
            else:
                st.error(f"DECISION: {decision}")
            st.info(f"Interest Rate: {interest}")
            
        # Logic Explanation for the User
        with st.expander("See Logic Breakdown"):
            st.write(f"**DTI Ratio:** {round(debt/income, 2)} (Weight: 40%)")
            st.write(f"**Stability:** {years} Years (Weight: 30%)")
            st.write(f"**History:** {int(history*100)}% (Weight: 30%)")