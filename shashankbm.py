import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Credit Risk Evaluator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR AESTHETICS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp header {
        background-color: #1E3D59;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {
        color: #1E3D59;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT PARAMETERS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/ICICI_Bank_Logo.svg/2560px-ICICI_Bank_Logo.svg.png", width=150)
    st.title("Credit Assessment Control")
    st.markdown("---")
    
    st.subheader("📝 Score Card Inputs (1-10)")
    
    # Inputs for the 5 Key Parameters
    p_financial = st.slider("Financial Ratios (Liquidity/Solvency)", 1, 10, 4, help="Current Ratio, Debt/EBITDA, Z-Score")
    p_industry = st.slider("Industry Risk", 1, 10, 5, help="Cyclicality, Competition, Regulatory environment")
    p_management = st.slider("Management Quality", 1, 10, 10, help="Governance, Experience, Group Support")
    p_market = st.slider("Market Position", 1, 10, 9, help="Market Share, Moat, Cost Leadership")
    p_collateral = st.slider("Collateral Coverage", 1, 10, 0, help="Security offered against the loan")

    st.markdown("---")
    st.caption("Adjust sliders to simulate different scenarios for Tata Steel.")

# --- CALCULATION LOGIC ---
# Weights defined in the report
weights = {
    "Financial Ratios": 0.30,
    "Industry Risk": 0.20,
    "Management Quality": 0.25,
    "Market Position": 0.15,
    "Collateral": 0.10
}

# Calculate Weighted Score
raw_scores = {
    "Financial Ratios": p_financial,
    "Industry Risk": p_industry,
    "Management Quality": p_management,
    "Market Position": p_market,
    "Collateral": p_collateral
}

final_score = sum(raw_scores[k] * weights[k] for k in weights)

# Decision Logic
if final_score >= 7.5:
    decision = "APPROVED (Unsecured)"
    color = "green"
elif final_score >= 6.0:
    decision = "REVIEW (Require Security)"
    color = "orange"
else:
    decision = "REJECT"
    color = "red"

# --- MAIN DASHBOARD LAYOUT ---

st.title("🏦 AI Credit Score Evaluation Dashboard")
st.markdown(f"### Borrower: **Tata Steel Limited** | Lender: **ICICI Bank**")
st.markdown("---")

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Altman Z-Score", value="1.75", delta="-0.15 vs Q3", help="< 1.8 indicates Distress Zone")
with col2:
    st.metric(label="Current Ratio", value="0.73", delta="-0.05", delta_color="inverse")
with col3:
    st.metric(label="Net Debt / EBITDA", value="3.55x", delta="+0.4x", delta_color="inverse")
with col4:
    st.metric(label="Piotroski F-Score", value="6 / 9", help="Indicates stable operational efficiency")

# --- ROW 1: SCORE VISUALIZATIONS ---
st.markdown("### 📊 AI Score Card Analysis")
c1, c2 = st.columns([1, 1])

with c1:
    # GRAPH 1: Gauge Chart for Final Score
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = final_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Aggregate Credit Score (0-10)"},
        delta = {'reference': 7.5, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E3D59"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#ffcccb'},
                {'range': [5, 7.5], 'color': '#ffe4b5'},
                {'range': [7.5, 10], 'color': '#90ee90'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': final_score}}))
    fig_gauge.update_layout(height=350, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Display Decision
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: {color}; color: white; border-radius: 5px;">
        <h3>Recommendation: {decision}</h3>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # GRAPH 2: Radar Chart for Parameter Balance
    df_radar = pd.DataFrame(dict(
        r=[p_financial, p_industry, p_management, p_market, p_collateral],
        theta=list(weights.keys())
    ))
    fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0,10])
    fig_radar.update_traces(fill='toself', line_color='#1E3D59')
    fig_radar.update_layout(
        title="Risk Parameter Balance",
        height=400,
        polar=dict(radialaxis=dict(visible=True, range=[0, 10]))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# --- ROW 2: FINANCIAL DEEP DIVE ---
st.markdown("### 📉 Financial & Trend Analysis")
c3, c4 = st.columns(2)

with c3:
    # GRAPH 3: Bar Chart - Borrower vs Industry Benchmark
    data_bench = {
        'Metric': ['Current Ratio', 'Interest Coverage', 'Debt/Equity', 'EBITDA Margin %'],
        'Tata Steel': [0.73, 3.2, 0.65, 14.5],
        'Industry Avg': [1.2, 4.5, 0.80, 12.0]
    }
    df_bench = pd.DataFrame(data_bench)
    df_bench_melt = df_bench.melt(id_vars='Metric', var_name='Entity', value_name='Value')
    
    fig_bar = px.bar(df_bench_melt, x='Metric', y='Value', color='Entity', barmode='group',
                     color_discrete_map={'Tata Steel': '#1E3D59', 'Industry Avg': '#A0A0A0'},
                     title="Borrower vs Industry Benchmarks")
    fig_bar.update_layout(height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    # GRAPH 4: Historical Credit Score Trend (Simulated)
    dates = pd.date_range(start='2023-01-01', periods=8, freq='Q')
    # Simulating a dip in score due to European operations drag
    scores = [7.2, 7.1, 6.8, 6.5, 6.2, 6.1, 6.0, final_score] 
    
    # CORRECTED (New Code)
fig_line = px.area(x=dates, y=scores, title="8-Quarter Credit Score Trend")
# Change 'fill_color' to 'fillcolor'
fig_line.update_traces(line_color='#1E3D59', fillcolor='rgba(30, 61, 89, 0.3)')
    fig_line.add_hline(y=7.5, line_dash="dash", line_color="green", annotation_text="Approval Threshold")
    fig_line.update_yaxes(range=[4, 10], title="Credit Score")
    fig_line.update_xaxes(title="Quarter")
    fig_line.update_layout(height=350)
    st.plotly_chart(fig_line, use_container_width=True)

# --- EXPANDER FOR DETAILS ---
with st.expander("ℹ️ View Detailed Methodology"):
    st.write("""
    **Methodology:**
    This AI-Scorecard aggregates weighted risks across 5 dimensions:
    1.  **Financial Ratios (30%):** Quantitative assessment of liquidity (Current Ratio) and solvency (Debt/EBITDA).
    2.  **Management Quality (25%):** Qualitative assessment of governance, group support, and execution history.
    3.  **Industry Risk (20%):** External factors including cyclicality and raw material price volatility.
    4.  **Market Position (15%):** Competitive advantage and scale.
    5.  **Collateral (10%):** Security coverage ratio. Unsecured loans score 0 here.
    """)
