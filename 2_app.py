import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEON | Credit Risk Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 🎨 CUSTOM NEON CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;600&family=Fira+Code:wght@400&display=swap');

    /* GLOBAL THEME */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }
    
    h1 {
        background: linear-gradient(90deg, #00f2ff, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
    }

    /* NEON CARDS */
    .neon-card {
        background: rgba(20, 20, 20, 0.6);
        border: 1px solid #333;
        border-left: 4px solid #00f2ff;
        border-radius: 10px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        transition: all 0.3s ease;
    }
    .neon-card:hover {
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.3);
        border-left-color: #ff00ff;
    }

    /* TERMINAL LOGS DESIGN (NEW) */
    .terminal-box {
        background-color: #0a0a0a;
        border: 1px solid #333;
        border-left: 4px solid #33ff00; /* Hacker Green Border */
        border-radius: 5px;
        padding: 20px;
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #e0e0e0;
        margin-top: 10px;
        box-shadow: inset 0 0 20px rgba(0, 20, 0, 0.8);
    }
    .log-line {
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 4px;
    }
    .log-time {
        color: #555;
        margin-right: 15px;
        font-size: 0.8rem;
    }
    .log-tag {
        color: #00f2ff;
        margin-right: 10px;
        font-weight: bold;
        min-width: 80px;
    }
    .log-val {
        color: #33ff00;
    }

    /* INPUT FIELDS */
    .stTextInput input, .stNumberInput input {
        background-color: #0a0a0a !important;
        color: #00f2ff !important;
        border: 1px solid #333 !important;
        font-family: 'Orbitron', monospace !important;
        border-radius: 0px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #00f2ff !important;
        box-shadow: 0 0 10px #00f2ff !important;
    }

    /* GLOWING BUTTON */
    .stButton button {
        background: transparent;
        border: 2px solid #00f2ff;
        color: #00f2ff;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 0px;
        transition: 0.3s;
        width: 100%;
        text-shadow: 0 0 5px #00f2ff;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    .stButton button:hover {
        background: #00f2ff;
        color: #000;
        box-shadow: 0 0 30px #00f2ff;
    }

    /* PLOTLY CHART BACKGROUNDS */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 🧠 LOGIC ENGINE ---
def calculate_score(income, debt, years_employed, history_pct):
    score = 0
    
    # 1. DTI Logic (Max 40 pts)
    if income == 0: dti = 100 
    else: dti = (debt / income)
    
    dti_pts = 0
    if dti < 0.2: dti_pts = 40
    elif dti < 0.4: dti_pts = 30
    elif dti < 0.6: dti_pts = 10
    
    # 2. Stability Logic (Max 30 pts)
    stab_pts = 10
    if years_employed >= 5: stab_pts = 30
    elif years_employed >= 2: stab_pts = 20
    
    # 3. History Logic (Max 30 pts)
    hist_pts = 0
    if history_pct >= 0.95: hist_pts = 30
    elif history_pct >= 0.85: hist_pts = 20
    elif history_pct >= 0.70: hist_pts = 10
    
    final_score = dti_pts + stab_pts + hist_pts
    return final_score, dti, dti_pts, stab_pts, hist_pts

def get_neon_status(score):
    if score >= 80:
        return "APPROVED", "PRIME RATE", "#39ff14" # Neon Green
    elif score >= 50:
        return "APPROVED", "SUB-PRIME", "#ff00ff" # Neon Pink
    else:
        return "REJECTED", "HIGH RISK", "#ff0000" # Neon Red

# --- 📊 CHART FUNCTIONS ---
def make_risk_donut(score, color):
    # Professional Donut Chart instead of Speedometer
    fig = go.Figure(data=[go.Pie(
        labels=['Score', 'Remaining'],
        values=[score, 100-score],
        hole=0.75, # Thinner ring looks more professional
        marker_colors=[color, '#1f1f1f'], # Neon fill vs Dark Grey background
        textinfo='none',
        hoverinfo='none',
        sort=False, # Don't reorder, keep Score first
        direction='clockwise'
    )])

    # Add Center Annotation
    fig.update_layout(
        annotations=[
            dict(
                text=str(int(score)), 
                x=0.5, y=0.55, 
                font_size=60, 
                font_family="Orbitron", 
                font_color=color, 
                showarrow=False
            ),
            dict(
                text="RISK SCORE", 
                x=0.5, y=0.35, 
                font_size=16, 
                font_family="Rajdhani", 
                font_color="#888", 
                showarrow=False
            )
        ],
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20),
        height=300
    )
    return fig

def make_radar(dti_pts, stab_pts, hist_pts):
    # Normalize to 100% for visual balance
    categories = ['DTI Ratio', 'Job Stability', 'Repayment Hist']
    
    # Max points: 40, 30, 30. We scale them to 10-100 for the chart visual
    values = [dti_pts, stab_pts, hist_pts]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Applicant Profile',
        line_color='#00f2ff',
        fillcolor='rgba(0, 242, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 40], color="#444"),
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(color="#888")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e0e0e0", family="Orbitron"),
        margin=dict(l=40, r=40, t=20, b=20),
        showlegend=False,
        height=300
    )
    return fig

# --- 🖥️ APP LAYOUT ---
st.title("NEON_RISK_ENGINE v2.0")
st.markdown("`SYSTEM STATUS: ONLINE` | `MODE: INTERACTIVE`")
st.write("")

# Sidebar
with st.sidebar:
    st.header("SYSTEM CONTROL")
    page = st.radio("SELECT MODULE:", ["SIMULATION", "DATABASE_ADMIN"])
    st.write("---")
    st.caption("SECURE CONNECTION ESTABLISHED")

if page == "SIMULATION":
    # INPUT SECTION
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<p style="color:#00f2ff">INCOME (SAR)</p>', unsafe_allow_html=True)
        income = st.number_input("", value=12000, step=1000, key="inc")
    with c2:
        st.markdown('<p style="color:#ff00ff">TOTAL DEBT (SAR)</p>', unsafe_allow_html=True)
        debt = st.number_input("", value=3000, step=500, key="dbt")
    with c3:
        st.markdown('<p style="color:#00f2ff">YEARS EMPLOYED</p>', unsafe_allow_html=True)
        years = st.number_input("", value=4, step=1, key="yrs")
    with c4:
        st.markdown('<p style="color:#ff00ff">HISTORY SCORE (%)</p>', unsafe_allow_html=True)
        history = st.slider("", 0, 100, 95, key="hst") / 100.0

    st.write("")
    if st.button("INITIATE ANALYSIS SEQUENCE"):
        # Calc
        score, dti, d_pts, s_pts, h_pts = calculate_score(income, debt, years, history)
        status, sub_status, color = get_neon_status(score)

        # RESULTS SECTION
        st.write("---")
        
        # 1. Main Status Banner
        st.markdown(f"""
        <div style="border: 2px solid {color}; background: rgba(0,0,0,0.8); border-radius: 0px; text-align: center; padding: 20px; box-shadow: 0 0 40px {color}40;">
            <h1 style="color: {color} !important; text-shadow: 0 0 20px {color}; margin: 0;">{status}</h1>
            <h3 style="color: #fff; margin-top: 10px;">TIER: {sub_status}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # 2. Charts
        g_col, r_col = st.columns([1, 1])
        
        with g_col:
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            st.plotly_chart(make_risk_donut(score, color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with r_col:
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: #00f2ff; margin-bottom: 0px;'>FACTOR ANALYSIS</h3>", unsafe_allow_html=True)
            st.plotly_chart(make_radar(d_pts, s_pts, h_pts), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. Data Breakdown (IMPROVED LOGS)
        st.write("")
        st.markdown("### 🖥️ KERNEL_OPERATIONS.log")
        
        # Generate fake milliseconds for realism
        now = datetime.datetime.now()
        t1 = now.strftime("%H:%M:%S:021")
        t2 = now.strftime("%H:%M:%S:145")
        t3 = now.strftime("%H:%M:%S:382")
        t4 = now.strftime("%H:%M:%S:899")
        t5 = now.strftime("%H:%M:%S:950")

        log_html = f"""
        <div class="terminal-box">
            <div class="log-line">
                <span class="log-time">[{t1}]</span> 
                <span class="log-tag">[INIT]</span> 
                <span>STARTING SEQUENCE...</span>
            </div>
            <div class="log-line">
                <span class="log-time">[{t2}]</span> 
                <span class="log-tag">[CALC]</span> 
                <span>DTI_RATIO COMPUTED: <span class="log-val">{int(dti*100)}%</span> (POINTS: {d_pts})</span>
            </div>
            <div class="log-line">
                <span class="log-time">[{t3}]</span> 
                <span class="log-tag">[VERIFY]</span> 
                <span>EMPLOYMENT_STABILITY CHECK: <span class="log-val">{years} YRS</span> (POINTS: {s_pts})</span>
            </div>
            <div class="log-line">
                <span class="log-time">[{t4}]</span> 
                <span class="log-tag">[AUDIT]</span> 
                <span>CREDIT_HISTORY ANALYSIS: <span class="log-val">{int(history*100)}%</span> (POINTS: {h_pts})</span>
            </div>
             <div class="log-line" style="border-bottom: none;">
                <span class="log-time">[{t5}]</span> 
                <span class="log-tag" style="color:{color}">[FINAL]</span> 
                <span style="color:{color}; font-weight:bold;">DECISION GENERATED: {status} (SCORE: {score}/100)</span>
            </div>
        </div>
        """
        st.markdown(log_html, unsafe_allow_html=True)

elif page == "DATABASE_ADMIN":
    st.title("ADMIN // DATABASE_VIEW")
    
    conn = sqlite3.connect('credit_risk.db')
    
    # Advanced Query
    query = """
    SELECT 
        a.id, 
        a.name, 
        a.monthly_income, 
        c.total_debt,
        (c.total_debt / a.monthly_income) as dti_ratio,
        l.repayment_on_time_pct
    FROM applicants a
    JOIN credit_bureau c ON a.id = c.applicant_id
    JOIN loan_history l ON a.id = l.applicant_id
    """
    df = pd.read_sql_query(query, conn)
    
    # INTERACTIVE SCATTER PLOT
    st.markdown("### MARKET ANALYSIS: INCOME vs DEBT")
    fig = px.scatter(
        df, 
        x="monthly_income", 
        y="total_debt", 
        color="dti_ratio",
        size="monthly_income",
        hover_data=["name"],
        color_continuous_scale=["#39ff14", "#ff00ff"],
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron", color="#00f2ff")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # RAW DATA
    st.markdown("### ENCRYPTED_RECORDS_TABLE")
    st.dataframe(df, use_container_width=True)
    
    conn.close()
