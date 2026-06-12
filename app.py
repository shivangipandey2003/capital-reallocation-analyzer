import streamlit as st
import plotly.graph_objects as go

# 1. System Page & Configuration Layer
st.set_page_config(
    page_title="Capital Reallocation Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Main Dashboard Headers
st.title("Amaara Grove: Capital Reallocation Analyzer")
st.markdown("Quantifying the **Cost of Doing Nothing** for distressed real estate assets.")
st.markdown("---")

# 3. Sidebar Input Parameter Layer
st.sidebar.header("Client Asset Inputs")
orig_price = st.sidebar.number_input("Original Purchase Price (INR)", value=10000000, step=500000)
curr_value = st.sidebar.number_input("Current Estimated Value (INR)", value=8000000, step=500000)
haircut = st.sidebar.slider("Distressed Sale Haircut (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
holding_cost = st.sidebar.number_input("Annual Holding Cost (INR)", value=50000, step=5000)

st.sidebar.header("Market Assumptions")
inflation_rate = st.sidebar.slider("Inflation Rate (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.5)
target_return = st.sidebar.slider("Amaara Grove Expected Return (%)", min_value=5.0, max_value=25.0, value=12.0, step=0.5)
horizon = st.sidebar.slider("Time Horizon (Years)", min_value=1, max_value=15, value=5, step=1)

# 4. Core Mathematical Processing Core
i = inflation_rate / 100.0
r = target_return / 100.0
h = haircut / 100.0

# Calculate initial liquid capital after exit haircut
liquid_capital = curr_value * (1.0 - h)

years = list(range(0, horizon + 1))
stagnant_path = []
reallocated_path = []

for t in years:
    # Formula 1: Stagnant Asset Wealth Decay
    stagnant_val = (curr_value - (holding_cost * t)) / ((1.0 + i) ** t)
    stagnant_path.append(stagnant_val)
    
    # Formula 2: Reallocated Performing Asset Accumulation
    reallocated_val = (liquid_capital * ((1.0 + r) ** t)) / ((1.0 + i) ** t)
    reallocated_path.append(reallocated_val)

# Extract Terminal Values
final_stagnant = stagnant_path[-1]
final_reallocated = reallocated_path[-1]
total_wealth_decay = curr_value - final_stagnant

# 5. Key Metrics Top Display Panel
col1, col2 = st.columns(2)
with col1:
    st.subheader("Scenario A: Hold Stalled Asset")
    st.metric(
        label=f"Real Value at Year {horizon}", 
        value=f"₹ {final_stagnant:,.0f}", 
        delta=f"-₹ {total_wealth_decay:,.0f} (Inflation & Costs)",
        delta_color="inverse"
    )
with col2:
    st.subheader("Scenario B: Amaara Grove")
    st.metric(
        label=f"Real Value at Year {horizon}", 
        value=f"₹ {final_reallocated:,.0f}", 
        delta=f"₹ {final_reallocated - liquid_capital:,.0f} (Net Growth)",
        delta_color="normal"
    )

st.markdown("---")
st.subheader("📈 Real Wealth Projection (Adjusted for Inflation)")

# 6. Interactive Plotly Graph Engine Layer
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years, y=stagnant_path, 
    mode='lines+markers', name='Status Quo (Doing Nothing)',
    line=dict(color='#dc2626', width=3), marker=dict(size=6)
))
fig.add_trace(go.Scatter(
    x=years, y=reallocated_path, 
    mode='lines+markers', name='Reallocated to Amaara Grove',
    line=dict(color='#16a34a', width=3), marker=dict(size=6)
))

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Real Wealth (INR)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.01),
    margin=dict(l=40, r=40, t=40, b=40),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)