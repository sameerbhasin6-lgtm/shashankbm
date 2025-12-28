import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Credit Risk Evaluator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}
.stApp header {
    background-color: #1E3D59;
}
h1, h2, h3 {
    color: #1E3D59;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
div[data-testid="stMetricValue"] {
    font-size: 24px;
    color: #1E3D59;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🏦 ICICI Bank")
    st.caption("Credit Assessment Control")
    st.markdown("---")

    st.subheader("📝 Score Card Inputs (0–10)")

    p_financial = st.slider(
        "Financial Ratios (Liquidity / Solvency)",
        1, 10, 4
    )

    p_industry = st.slider(
        "Industry Risk",
        1, 10, 5
    )

    p_management = st.slider(
        "Management Quality",
        1, 10, 10
    )

    p_market = st.slider(
        "Market Position",
        1, 10, 9
    )

    # ✅ FIXED: range includes 0
    p_collateral = st.slider(
        "Collateral Coverage",
        0, 10, 0,
        help="0 = Unsecured loan"
    )

    st.markdown("---")
    st.info("Adjust sliders to simulate different risk scenarios.")

# --------------------------------------------------
# SCORING LOGIC
# --------------------------------------------------
weights = {
    "Financial Ratios": 0.30,
    "Industry Risk": 0.20,
    "Management Quality": 0.25,
    "Market Position": 0.15,
    "Collateral": 0.10
}

final_score = (
    p_financial * weights["Financial Ratios"]
    + p_industry * weights["Industry Risk"]
    + p_management * weights["Management Quality"]
    + p_market * weights["Market Position"]
    + p_collateral * weights["Collateral"]
)

if final_score >= 7.5:
    decision = "APPROVED (Unsecured)"
    color_code = "#28a745"
elif final_score >= 6.0:
    decision = "REVIEW (Require Security)"
    color_code = "#ffc107"
else:
    decision = "REJECT"
    color_code = "#dc3545"

# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------
st.title("AI Credit Score Evaluation Dashboard")
st.markdown("### Borrower: **Tata Steel Limited** | Lender: **ICICI Bank**")
st.markdown("---")

# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Altman Z-Score", "1.75", "-0.15 vs Q3")

with c2:
    st.metric("Current Ratio", "0.73", "-0.05", delta_color="inverse")

with c3:
    st.metric("Net Debt / EBITDA", "3.55x", "+0.4x", delta_color="inverse")

with c4:
    st.metric("Piotroski F-Score", "6 / 9")

st.markdown("### 📊 AI Score Card Analysis")

# --------------------------------------------------
# ROW 1 – SCORE VISUALS
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_score,
        title={"text": "Aggregate Credit Score (0–10)"},
        gauge={
            "axis": {"range": [0, 10]},
            "bar": {"color": "#1E3D59"},
            "steps": [
                {"range": [0, 5], "color": "#ffcccc"},
                {"range": [5, 7.5], "color": "#ffe4b5"},
                {"range": [7.5, 10], "color": "#90ee90"}
            ]
        }
    ))
    fig_gauge.update_layout(height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown(
        f"""
        <div style="padding:15px;text-align:center;
        background:{color_code};color:white;border-radius:8px;">
        <h3>Recommendation: {decision}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    df_radar = pd.DataFrame({
        "Score": [
            p_financial,
            p_industry,
            p_management,
            p_market,
            p_collateral
        ],
        "Parameter": list(weights.keys())
    })

    fig_radar = px.line_polar(
        df_radar,
        r="Score",
        theta="Parameter",
        line_close=True,
        range_r=[0, 10]
    )
    fig_radar.update_traces(fill="toself", line_color="#1E3D59")
    fig_radar.update_layout(height=400, title="Risk Parameter Balance")
    st.plotly_chart(fig_radar, use_container_width=True)

# --------------------------------------------------
# ROW 2 – FINANCIAL ANALYSIS
# --------------------------------------------------
st.markdown("---")
st.markdown("### 📉 Financial & Trend Analysis")

c3, c4 = st.columns(2)

with c3:
    df_bench = pd.DataFrame({
        "Metric": ["Current Ratio", "Interest Coverage", "Debt/Equity", "EBITDA Margin %"],
        "Tata Steel": [0.73, 3.2, 0.65, 14.5],
        "Industry Avg": [1.2, 4.5, 0.8, 12.0]
    }).melt(id_vars="Metric", var_name="Entity", value_name="Value")

    fig_bar = px.bar(
        df_bench,
        x="Metric",
        y="Value",
        color="Entity",
        barmode="group",
        title="Borrower vs Industry Benchmarks"
    )
    fig_bar.update_layout(height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    dates = pd.date_range(start="2023-01-01", periods=8, freq="Q")
    scores = [7.2, 7.1, 6.8, 6.5, 6.2, 6.1, 6.0, final_score]

    fig_line = px.area(
        x=dates,
        y=scores,
        title="8-Quarter Credit Score Trend"
    )

    # ✅ FIXED: correct Plotly property name
    fig_line.update_traces(
        line_color="#1E3D59",
        fillcolor="rgba(30, 61, 89, 0.3)"
    )

    fig_line.add_hline(
        y=7.5,
        line_dash="dash",
        line_color="green",
        annotation_text="Approval Threshold"
    )

    fig_line.update_yaxes(range=[4, 10], title="Credit Score")
    fig_line.update_xaxes(title="Quarter")
    fig_line.update_layout(height=350)
    st.plotly_chart(fig_line, use_container_width=True)

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------
with st.expander("ℹ️ View Detailed Methodology"):
    st.write("""
    This AI Credit Score aggregates weighted risk across:
    • Financial strength  
    • Industry environment  
    • Management quality  
    • Market positioning  
    • Collateral support  
    """)

