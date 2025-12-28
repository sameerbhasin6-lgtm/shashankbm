import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ICICI Credit Assessment",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM BRANDING & CSS ---
# ICICI Colors: Dark Blue (#052962), Orange (#F27D21)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    h1, h2, h3 {
        color: #052962;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #F27D21;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    div[data-testid="stSidebarUserContent"] {
        background-color: #ffffff;
        padding: 20px;
        border-right: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏦 ICICI Bank")
    st.markdown("### Corporate Risk Unit")
    st.markdown("---")
    
    st.write("**Risk Parameter Inputs (1-10)**")
    
    # Sliders with specific keys to prevent state issues
    p_financial = st.slider("Financial Health (Liquidity/Solvency)", 1, 10, 4)
    p_industry = st.slider("Industry Outlook", 1, 10, 5)
    p_management = st.slider("Management Quality", 1, 10, 10)
    p_market = st.slider("Market Dominance", 1, 10, 9)
    p_collateral = st.slider("Collateral Coverage", 1, 10, 0)

    st.markdown("---")
    st.info("ℹ️ **Note:** Unsecured loans automatically score 0 on Collateral.")

# --- SCORING ENGINE ---
# Weights
w_fin = 0.30
w_ind = 0.20
w_mgt = 0.25
w_mkt = 0.15
w_col = 0.10

# Calculate Score
score = (p_financial * w_fin) + (p_industry * w_ind) + \
        (p_management * w_mgt) + (p_market * w_mkt) + (p_collateral * w_col)

# Decision Logic
if score >= 7.5:
    status = "APPROVED"
    sub_status = "Clean Unsecured"
    box_color = "#28a745" # Green
elif score >= 6.0:
    status = "REVIEW REQUIRED"
    sub_status = "Seek Security / Covenants"
    box_color = "#F27D21" # ICICI Orange
else:
    status = "REJECT"
    sub_status = "High Risk Exposure"
    box_color = "#dc3545" # Red

# --- MAIN DASHBOARD ---

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("Credit Appraisal Memo")
    st.markdown("#### Borrower: **Tata Steel Ltd** | Facility: **₹8,700 Cr (Unsecured)**")

# Decision Banner
st.markdown(f"""
<div style="background-color: {box_color}; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px;">
    <h2 style="color: white; margin:0;">Recommendation: {status}</h2>
    <p style="margin:0; font-size: 18px; opacity: 0.9;">Action: {sub_status} (Score: {score:.2f}/10)</p>
</div>
""", unsafe_allow_html=True)

# Key Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Altman Z-Score", "1.75", "-0.15 (Distress)")
c2.metric("Current Ratio", "0.73", "-0.2 vs Peers")
c3.metric("Net Debt / EBITDA", "3.55x", "+0.4x QoQ")
c4.metric("Piotroski F-Score", "6/9", "Stable")

st.markdown("---")

# --- VISUALIZATIONS ---

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Risk Parameter Breakdown")
    # Radar Chart
    categories = ['Financials', 'Industry', 'Management', 'Market Pos.', 'Collateral']
    values = [p_financial, p_industry, p_management, p_market, p_collateral]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(5, 41, 98, 0.2)', # ICICI Blue transparent
        line=dict(color='#052962'),
        name='Tata Steel'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        height=350,
        margin=dict(t=20, b=20, l=40, r=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("2. Score Trend Analysis")
    # Area Chart (Historical)
    dates = ['Q1-23', 'Q2-23', 'Q3-23', 'Q4-23', 'Q1-24', 'Q2-24', 'Q3-24', 'Current']
    scores = [7.2, 7.1, 6.9, 6.5, 6.3, 6.1, 6.0, score]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=dates, 
        y=scores, 
        mode='lines+markers',
        fill='tozeroy',  # Fills to the x-axis
        name='Credit Score',
        # --- THE FIX: Explicit Dictionary for Line and Fill ---
        line=dict(color='#052962', width=3),
        fillcolor='rgba(5, 41, 98, 0.1)' # Correct property name
    ))
    
    # Add Threshold Line
    fig_trend.add_hline(y=7.5, line_dash="dash", line_color="#28a745", annotation_text="Approval Limit")
    fig_trend.add_hline(y=6.0, line_dash="dash", line_color="#F27D21", annotation_text="Review Limit")
    
    fig_trend.update_layout(
        yaxis=dict(range=[4, 10], title="AI Score"),
        height=350,
        margin=dict(t=20, b=20, l=40, r=40)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Comparative Analysis
st.subheader("3. Benchmark Comparison")
bench_data = {
    'Metric': ['Current Ratio', 'Debt/EBITDA', 'Interest Cov.', 'EBITDA Margin'],
    'Tata Steel': [0.73, 3.55, 3.2, 14.5],
    'Peer Avg': [1.3, 2.5, 5.0, 12.0]
}
df_bench = pd.DataFrame(bench_data)
df_melt = df_bench.melt(id_vars="Metric", var_name="Entity", value_name="Value")

fig_bar = px.bar(
    df_melt, x="Metric", y="Value", color="Entity", barmode="group",
    color_discrete_map={'Tata Steel': '#052962', 'Peer Avg': '#A0A0A0'}
)
fig_bar.update_layout(height=350, margin=dict(t=20))
st.plotly_chart(fig_bar, use_container_width=True)
