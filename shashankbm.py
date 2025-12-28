import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Credit Risk Evaluation | Tata Steel",
    page_icon="🏦",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
h1, h2, h3 {
    color: #1E3D59;
    font-family: 'Segoe UI', sans-serif;
}
.metric-box {
    background-color: white;
    padding: 18px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    text-align: center;
}
.recommend-reject {
    background-color: #ffe5e5;
    color: #b30000;
    padding: 18px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🏦 AI-Based Credit Evaluation Dashboard")
st.subheader("Borrower: Tata Steel Limited | Lender: ICICI Bank")

# ---------------------------------------------------
# KEY DETAILS
# ---------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-box"><h3>Loan Amount</h3><h2>₹8,700 Cr</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-box"><h3>Facility Type</h3><h2>Unsecured</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-box"><h3>Net Debt / EBITDA</h3><h2>3.55x</h2></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-box"><h3>Altman Z-Score</h3><h2>1.75</h2></div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RISKOMETER (AI CREDIT SCORE)
# ---------------------------------------------------
st.markdown("## 🔴 AI Credit Riskometer")

ai_score = 6.05  # from your analysis

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ai_score,
    number={'font': {'size': 50}},
    title={'text': "AI Credit Score (Out of 10)"},
    gauge={
        'axis': {'range': [0, 10]},
        'bar': {'color': "darkred"},
        'steps': [
            {'range': [0, 4], 'color': '#ff4d4d'},
            {'range': [4, 7.5], 'color': '#ffcc00'},
            {'range': [7.5, 10], 'color': '#4CAF50'}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': 7.5
        }
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

# ---------------------------------------------------
# FINANCIAL RATIOS BAR CHART
# ---------------------------------------------------
st.markdown("## 📊 Key Financial Ratios")

ratio_df = pd.DataFrame({
    "Metric": [
        "Current Ratio",
        "Quick Ratio",
        "Debt-to-Equity",
        "Interest Coverage",
        "Net Debt / EBITDA"
    ],
    "Value": [0.73, 0.24, 0.65, 3.2, 3.55]
})

fig_ratios = px.bar(
    ratio_df,
    x="Metric",
    y="Value",
    text="Value",
    color="Value",
    color_continuous_scale="RdYlGn_r",
    title="Liquidity & Leverage Profile"
)

st.plotly_chart(fig_ratios, use_container_width=True)

# ---------------------------------------------------
# ALTMAN Z-SCORE COMPONENTS
# ---------------------------------------------------
st.markdown("## 📉 Altman Z-Score Component Analysis")

z_df = pd.DataFrame({
    "Component": [
        "Working Capital / Assets",
        "Retained Earnings / Assets",
        "EBIT / Assets",
        "Market Value / Liabilities",
        "Sales / Assets"
    ],
    "Contribution": [-0.10, 0.40, 0.06, 0.70, 0.90]
})

fig_z = px.bar(
    z_df,
    x="Component",
    y="Contribution",
    color="Contribution",
    color_continuous_scale="RdYlGn",
    title="Drivers of Altman Z-Score"
)

st.plotly_chart(fig_z, use_container_width=True)

# ---------------------------------------------------
# AI SCORECARD BREAKDOWN
# ---------------------------------------------------
st.markdown("## 🤖 AI Credit Scorecard Breakdown")

scorecard_df = pd.DataFrame({
    "Risk Factor": [
        "Financial Ratios",
        "Industry Risk",
        "Management Quality",
        "Market Position",
        "Collateral Coverage"
    ],
    "Score": [4, 5, 10, 9, 0]
})

fig_scorecard = px.pie(
    scorecard_df,
    names="Risk Factor",
    values="Score",
    hole=0.5,
    title="AI Risk Contribution Mix"
)

st.plotly_chart(fig_scorecard, use_container_width=True)

# ---------------------------------------------------
# DEBT STRUCTURE VISUAL
# ---------------------------------------------------
st.markdown("## 🧾 Debt Structure Snapshot")

debt_df = pd.DataFrame({
    "Type": ["Existing Debt", "Proposed Loan"],
    "Amount (₹ Cr)": [87000, 8700]
})

fig_debt = px.bar(
    debt_df,
    x="Type",
    y="Amount (₹ Cr)",
    color="Type",
    title="Proposed Loan as % of Total Debt"
)

st.plotly_chart(fig_debt, use_container_width=True)

# ---------------------------------------------------
# FINAL RECOMMENDATION
# ---------------------------------------------------
st.markdown("## ❌ Final Credit Recommendation")

st.markdown("""
<div class="recommend-reject">
REJECT – As Proposed<br><br>
The unsecured structure introduces excessive downside risk given:
<ul>
<li>Negative working capital</li>
<li>Net Debt / EBITDA above 3.0x</li>
<li>Altman Z-Score in Grey/Distress zone</li>
<li>High single-borrower concentration</li>
</ul>
<strong>Recommended Alternative:</strong> Secured, syndicated term loan with asset charge and tighter covenants.
</div>
""", unsafe_allow_html=True)
