import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Amaara Grove – Capital Reallocation Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    .step-box {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        margin-bottom: 16px;
        border-top: 4px solid #2563eb;
    }
    .step-box-red   { border-top-color: #dc2626; }
    .step-box-green { border-top-color: #16a34a; }
    .step-box-amber { border-top-color: #f59e0b; }
    .step-box-blue  { border-top-color: #2563eb; }

    .step-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 4px;
    }
    .big-number {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1e3a5f;
        line-height: 1.1;
    }
    .big-number-green { color: #16a34a; }
    .big-number-red   { color: #dc2626; }
    .big-number-blue  { color: #2563eb; }

    .sub-note {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 6px;
        line-height: 1.5;
    }
    .arrow-connector {
        font-size: 2rem;
        color: #94a3b8;
        text-align: center;
        padding: 0 4px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1e3a5f;
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 8px 14px;
        border-radius: 0 8px 8px 0;
        margin: 24px 0 14px 0;
    }
    .callout-green {
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 12px 0;
    }
    .callout-red {
        background: #fef2f2;
        border: 1.5px solid #fca5a5;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 12px 0;
    }
    .callout-amber {
        background: #fffbeb;
        border: 1.5px solid #fcd34d;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
            padding: 28px 36px; border-radius: 14px; margin-bottom: 28px;'>
    <h1 style='color:white; margin:0; font-size:1.9rem; font-weight:800;'>
        🏡 Amaara Grove
    </h1>
    <h2 style='color:#bfdbfe; margin:6px 0 0 0; font-size:1.1rem; font-weight:400;'>
        Capital Reallocation Analyzer
    </h2>
    <p style='color:#93c5fd; margin:10px 0 0 0; font-size:0.9rem;'>
        A step-by-step breakdown of how a distressed asset is converted into
        a high-yield investment — and how every rupee is recovered.
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR INPUTS
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style='background:linear-gradient(135deg,#1e3a5f,#2563eb);
            padding:12px 16px; border-radius:8px; margin-bottom:14px;'>
    <h3 style='color:white; margin:0; font-size:0.95rem;'>⚙️ Input Parameters</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🏚️ Distressed Asset")

orig_price = st.sidebar.number_input(
    "Original Purchase Price (INR)",
    value=10_000_000, step=500_000, format="%d",
    help="What the investor originally paid — this anchors the exit price."
)
curr_value = st.sidebar.number_input(
    "Current Market Value (INR)",
    value=8_000_000, step=500_000, format="%d",
    help="What the asset is worth today in the open market."
)
exit_premium_pct = st.sidebar.slider(
    "Exit Premium over Original Price (%)",
    min_value=0.0, max_value=30.0, value=10.0, step=1.0,
    help="We offer the investor this % ABOVE their original purchase price."
)
haircut_pct = st.sidebar.slider(
    "Transaction / Distress Haircut (%)",
    min_value=0.0, max_value=20.0, value=5.0, step=0.5,
    help="Broker fees, registration costs, urgency discount."
)
holding_cost = st.sidebar.number_input(
    "Annual Holding Cost of Distressed Asset (INR)",
    value=50_000, step=5_000, format="%d"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏗️ Amaara Grove Project")

project_value = st.sidebar.number_input(
    "Total Amaara Grove Project Value (INR)",
    value=50_000_000, step=1_000_000, format="%d",
    help="Total capital required / committed to Amaara Grove (e.g. ₹5 Cr)."
)
quarterly_recovery_pct = st.sidebar.slider(
    "Quarterly Recovery Rate (% of Project Value)",
    min_value=1.0, max_value=20.0, value=5.0, step=0.5,
    help="Each quarter this % of the TOTAL project value is recovered."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Market Assumptions")

inflation_rate = st.sidebar.slider(
    "Inflation Rate (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.5
)
target_return = st.sidebar.slider(
    "Amaara Grove Expected Annual Return (%)",
    min_value=5.0, max_value=30.0, value=12.0, step=0.5
)

# ══════════════════════════════════════════════════════════════════════════════
# CORE CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════

ep = exit_premium_pct / 100.0
h  = haircut_pct / 100.0
i  = inflation_rate / 100.0
r  = target_return / 100.0

# Step 1: Exit price anchored to ORIGINAL purchase price
gross_exit_price     = orig_price * (1.0 + ep)
transaction_costs    = gross_exit_price * h
net_capital_deployed = gross_exit_price * (1.0 - h)
capital_gap          = project_value - net_capital_deployed

# Step 2: Quarterly recovery schedule until FULL project value recovered
quarterly_payout_amount = project_value * (quarterly_recovery_pct / 100.0)

repayment_rows = []
cumulative = 0.0
quarters_to_full_recovery = None
q = 0

while cumulative < project_value:
    q += 1
    cumulative += quarterly_payout_amount
    year_num = math.ceil(q / 4)
    repayment_rows.append({
        "Quarter No.": q,
        "Label": f"Q{q} (Yr {year_num})",
        "Quarterly Payout (INR)": quarterly_payout_amount,
        "Cumulative Recovered (INR)": min(cumulative, project_value),
        "% of Project Value Recovered": min((cumulative / project_value) * 100, 100.0),
        "% of Investor's Capital Recovered": (
            min((cumulative / net_capital_deployed) * 100, 100.0)
            if net_capital_deployed > 0 else 0
        ),
        "Status": "✅ Fully Recovered" if cumulative >= project_value else "In Progress"
    })
    if quarters_to_full_recovery is None and cumulative >= project_value:
        quarters_to_full_recovery = q

repayment_df = pd.DataFrame(repayment_rows)
total_quarters       = len(repayment_df)
total_years_recovery = math.ceil(total_quarters / 4)

# Step 3: Wealth trajectory (inflation-adjusted)
horizon = total_years_recovery + 2
years   = list(range(0, horizon + 1))
stagnant_path    = []
reallocated_path = []

for t in years:
    stagnant_val    = (curr_value - holding_cost * t) / ((1.0 + i) ** t)
    reallocated_val = (net_capital_deployed * ((1.0 + r) ** t)) / ((1.0 + i) ** t)
    stagnant_path.append(stagnant_val)
    reallocated_path.append(reallocated_val)

final_stagnant    = stagnant_path[-1]
final_reallocated = reallocated_path[-1]
total_wealth_decay = curr_value - final_stagnant
opp_gap            = final_reallocated - final_stagnant
investor_stake_pct = (net_capital_deployed / project_value) * 100 if project_value > 0 else 0

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — THE DISTRESSED ASSET
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-title">📋 Step 1 — Understanding the Distressed Asset</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="step-box step-box-red">
        <div class="step-label">What Investor Paid</div>
        <div class="big-number big-number-red">₹ {orig_price/1e7:.2f} Cr</div>
        <div class="sub-note">Original purchase price.<br>
        This is the investor's <b>cost anchor</b> — they will not sell below this.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    loss_pct = ((orig_price - curr_value) / orig_price) * 100
    st.markdown(f"""
    <div class="step-box step-box-red">
        <div class="step-label">Current Market Value</div>
        <div class="big-number big-number-red">₹ {curr_value/1e7:.2f} Cr</div>
        <div class="sub-note">What the market values it at today.<br>
        <b>↓ {loss_pct:.1f}% below what they paid.</b><br>
        Investor is sitting on a paper loss.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="step-box step-box-amber">
        <div class="step-label">Annual Holding Cost</div>
        <div class="big-number" style="color:#b45309;">₹ {holding_cost:,.0f}</div>
        <div class="sub-note">Maintenance, taxes, opportunity cost.<br>
        Every year of inaction costs money on top of inflation erosion.</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="step-box step-box-red">
        <div class="step-label">The Problem</div>
        <div class="big-number big-number-red" style="font-size:1.3rem;">Asset is Stalled</div>
        <div class="sub-note">
        • No rental income<br>
        • No appreciation<br>
        • Losing value to inflation<br>
        • Holding costs accumulating<br>
        <b>Doing nothing = guaranteed loss</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — HOW WE STRUCTURE THE EXIT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-title">💡 Step 2 — How We Structure the Exit</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="callout-green">
    <b style='color:#166534;'>🎯 Key Principle:</b>
    <span style='color:#166534;'>
    We price the exit based on the investor's <b>original purchase price
    (₹{orig_price/1e7:.1f} Cr)</b>, not the depressed current market value
    (₹{curr_value/1e7:.1f} Cr). This way the investor feels they've made money —
    not taken a loss — making them more likely to agree.
    </span>
</div>
""", unsafe_allow_html=True)

e1, e_arr1, e2, e_arr2, e3 = st.columns([3, 0.5, 3, 0.5, 3])

with e1:
    st.markdown(f"""
    <div class="step-box step-box-red">
        <div class="step-label">Starting Point</div>
        <div class="big-number big-number-red">₹ {orig_price/1e7:.2f} Cr</div>
        <div class="sub-note">Investor's original cost<br>(what they anchor expectations to)</div>
    </div>
    """, unsafe_allow_html=True)

with e_arr1:
    st.markdown(
        "<div class='arrow-connector' style='margin-top:30px;'>→</div>",
        unsafe_allow_html=True
    )

with e2:
    premium_amount = orig_price * ep
    st.markdown(f"""
    <div class="step-box step-box-blue">
        <div class="step-label">+ Exit Premium ({exit_premium_pct:.0f}% on Original Price)</div>
        <div class="big-number big-number-blue">₹ {gross_exit_price/1e7:.2f} Cr</div>
        <div class="sub-note">
        We offer <b>+{exit_premium_pct:.0f}%</b> over what they paid.<br>
        That's an extra <b>₹ {premium_amount/1e5:.0f} Lakhs</b> as a sweetener.<br>
        <b>Investor sees a profit — not a loss.</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with e_arr2:
    st.markdown(
        "<div class='arrow-connector' style='margin-top:30px;'>→</div>",
        unsafe_allow_html=True
    )

with e3:
    st.markdown(f"""
    <div class="step-box step-box-green">
        <div class="step-label">Net Capital We Deploy (after {haircut_pct:.1f}% transaction costs)</div>
        <div class="big-number big-number-green">₹ {net_capital_deployed/1e7:.2f} Cr</div>
        <div class="sub-note">
        Transaction costs: <b>₹ {transaction_costs/1e5:.1f} L</b><br>
        This is the <b>actual amount</b> that goes into Amaara Grove.<br>
        Investor receives full ₹ {gross_exit_price/1e7:.2f} Cr from us.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Waterfall chart
st.markdown("#### 🔢 Price Walk — From Investor's Cost to Deployed Capital")

fig_wf = go.Figure(go.Waterfall(
    orientation="v",
    measure=["absolute", "relative", "relative", "total"],
    x=[
        "Investor's\nOriginal Price",
        f"+{exit_premium_pct:.0f}% Premium\n(sweetener)",
        f"−{haircut_pct:.1f}% Transaction\nCosts",
        "Net Capital\nDeployed"
    ],
    y=[orig_price, orig_price * ep, -transaction_costs, 0],
    text=[
        f"₹{orig_price/1e7:.2f} Cr",
        f"+₹{(orig_price*ep)/1e5:.1f} L",
        f"−₹{transaction_costs/1e5:.1f} L",
        f"₹{net_capital_deployed/1e7:.2f} Cr"
    ],
    textposition="outside",
    connector={"line": {"color": "#94a3b8", "width": 1.5, "dash": "dot"}},
    increasing={"marker": {"color": "#16a34a"}},
    decreasing={"marker": {"color": "#dc2626"}},
    totals={"marker": {"color": "#2563eb"}}
))
fig_wf.update_layout(
    yaxis_title="Amount (INR)",
    plot_bgcolor="#f9fafb",
    height=340,
    margin=dict(l=40, r=40, t=30, b=40),
    yaxis=dict(tickformat=",.0f")
)
st.plotly_chart(fig_wf, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — AMAARA GROVE PROJECT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-title">🏗️ Step 3 — Amaara Grove Project Overview</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown(f"""
    <div class="step-box step-box-blue">
        <div class="step-label">Total Project Value</div>
        <div class="big-number big-number-blue">₹ {project_value/1e7:.1f} Cr</div>
        <div class="sub-note">Total capital committed to<br>Amaara Grove project.</div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="step-box step-box-green">
        <div class="step-label">Capital We Deploy (from distressed exit)</div>
        <div class="big-number big-number-green">₹ {net_capital_deployed/1e7:.2f} Cr</div>
        <div class="sub-note">= <b>{investor_stake_pct:.1f}%</b> of total project.<br>
        This is the investor's funds now working<br>productively.</div>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown(f"""
    <div class="step-box step-box-amber">
        <div class="step-label">Additional Capital Needed</div>
        <div class="big-number" style="color:#b45309;">₹ {capital_gap/1e7:.2f} Cr</div>
        <div class="sub-note">Remaining {100 - investor_stake_pct:.1f}% of project to be<br>
        funded from other sources.</div>
    </div>
    """, unsafe_allow_html=True)

with p4:
    st.markdown(f"""
    <div class="step-box step-box-blue">
        <div class="step-label">Quarterly Recovery (per quarter)</div>
        <div class="big-number big-number-blue">₹ {quarterly_payout_amount/1e5:.1f} L</div>
        <div class="sub-note">= <b>{quarterly_recovery_pct:.1f}%</b> of ₹{project_value/1e7:.0f} Cr<br>
        paid back every quarter until all<br>
        ₹{project_value/1e7:.0f} Cr is fully recovered.</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — QUARTERLY RECOVERY SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div class="section-title">📅 Step 4 — Quarterly Recovery Schedule '
    f'(Until Full ₹{project_value/1e7:.0f} Cr Recovered)</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="callout-green">
    <b style='color:#166534;'>🎯 Recovery Goal:</b>
    <span style='color:#166534;'>
    We recover the <b>entire ₹{project_value/1e7:.0f} Cr project value</b> at
    <b>₹{quarterly_payout_amount/1e5:.1f} L per quarter</b>
    ({quarterly_recovery_pct:.1f}% of project value). This continues for
    <b>{quarters_to_full_recovery} quarters (~{total_years_recovery} years)</b>
    until every rupee of the ₹{project_value/1e7:.0f} Cr is returned.
    </span>
</div>
""", unsafe_allow_html=True)

# Milestone cards
mc1, mc2, mc3, mc4 = st.columns(4)
milestones = [25, 50, 75, 100]
colors     = ["#f59e0b", "#3b82f6", "#8b5cf6", "#16a34a"]

for col, ms, color in zip([mc1, mc2, mc3, mc4], milestones, colors):
    target_q = None
    for _, row in repayment_df.iterrows():
        if row["% of Project Value Recovered"] >= ms:
            target_q  = int(row["Quarter No."])
            target_yr = math.ceil(target_q / 4)
            amount_at = row["Cumulative Recovered (INR)"]
            break
    if target_q:
        with col:
            st.markdown(f"""
            <div class="step-box" style="border-top-color:{color};">
                <div class="step-label">{ms}% Recovered</div>
                <div class="big-number" style="color:{color};">Q{target_q}</div>
                <div class="sub-note">Year {target_yr}<br>
                ₹ {amount_at/1e7:.2f} Cr recovered</div>
            </div>
            """, unsafe_allow_html=True)

# Recovery chart
fig_rec = go.Figure()

bar_colors = [
    "#16a34a" if row["% of Project Value Recovered"] >= 100 else "#2563eb"
    for _, row in repayment_df.iterrows()
]

fig_rec.add_trace(go.Bar(
    x=repayment_df["Label"],
    y=repayment_df["Quarterly Payout (INR)"],
    name=f"Quarterly Payout (₹{quarterly_payout_amount/1e5:.1f} L each)",
    marker_color=bar_colors,
    opacity=0.85,
    hovertemplate="<b>%{x}</b><br>Payout: ₹%{y:,.0f}<extra></extra>"
))

fig_rec.add_trace(go.Scatter(
    x=repayment_df["Label"],
    y=repayment_df["Cumulative Recovered (INR)"],
    mode="lines+markers",
    name="Cumulative Recovered",
    line=dict(color="#f59e0b", width=3),
    marker=dict(size=6),
    yaxis="y2",
    hovertemplate="<b>%{x}</b><br>Cumulative: ₹%{y:,.0f}<extra></extra>"
))

fig_rec.add_hline(
    y=project_value,
    line_dash="dash", line_color="#dc2626", line_width=2,
    annotation_text=f"Full Recovery — ₹{project_value/1e7:.0f} Cr",
    annotation_position="top left",
    annotation_font_color="#dc2626",
    yref="y2"
)

fig_rec.add_hline(
    y=net_capital_deployed,
    line_dash="dot", line_color="#2563eb", line_width=1.5,
    annotation_text=f"Investor's Capital — ₹{net_capital_deployed/1e7:.2f} Cr",
    annotation_position="bottom right",
    annotation_font_color="#2563eb",
    yref="y2"
)

fig_rec.update_layout(
    xaxis=dict(title="Quarter", tickangle=-55),
    yaxis=dict(
        title="Quarterly Payout (INR)",
        showgrid=True, gridcolor="#e5e7eb", tickformat=",.0f"
    ),
    yaxis2=dict(
        title="Cumulative Recovered (INR)",
        overlaying="y", side="right",
        showgrid=False, tickformat=",.0f"
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=40, r=80, t=60, b=140),
    hovermode="x unified",
    plot_bgcolor="#f9fafb",
    height=480
)
st.plotly_chart(fig_rec, use_container_width=True)

# ── Full Recovery Table (Collapsible) ─────────────────────────────────────────
with st.expander(f"📋 View Full Recovery Table — All {total_quarters} Quarters"):

    # 1. Build display df with a clean integer index
    display_df_show = repayment_df[[
        "Label",
        "Quarterly Payout (INR)",
        "Cumulative Recovered (INR)",
        "% of Project Value Recovered",
        # "% of Investor's Capital Recovered",
        "Status"
    ]].copy().reset_index(drop=True)

    # 2. Save NUMERIC % column BEFORE any formatting or renaming
    pct_recovered_numeric = display_df_show["% of Project Value Recovered"].copy()

    # 3. Format display columns
    display_df_show["Quarterly Payout (INR)"] = display_df_show[
        "Quarterly Payout (INR)"
    ].apply(lambda x: f"₹ {x:,.0f}")

    display_df_show["Cumulative Recovered (INR)"] = display_df_show[
        "Cumulative Recovered (INR)"
    ].apply(lambda x: f"₹ {x:,.0f}")

    display_df_show["% of Project Value Recovered"] = display_df_show[
        "% of Project Value Recovered"
    ].apply(lambda x: f"{x:.1f}%")

    # display_df_show["% of Investor's Capital Recovered"] = display_df_show[
    #     "% of Investor's Capital Recovered"
    # ].apply(lambda x: f"{x:.1f}%")

    # 4. Rename columns AFTER formatting
    display_df_show.columns = [
        "Quarter",
        "Quarterly Payout",
        "Cumulative Recovered",
        f"% of ₹{project_value/1e7:.0f} Cr Recovered",
        # "% of Investor Capital Recovered",
        "Status"
    ]

    # 5. Style function — uses positional lookup (immune to column renames)
    def highlight_recovered(row):
        pct = pct_recovered_numeric.iloc[row.name]
        if pct >= 100.0:
            return ["background-color: #dcfce7; color: black; font-weight: bold"] * len(row)
        elif pct >= 75:
            return ["background-color: #fef9c3; color: black"] * len(row)
        elif pct >= 50:
            return ["background-color: #eff6ff; color: black"] * len(row)
        return [""] * len(row)

    st.dataframe(
        display_df_show.style.apply(highlight_recovered, axis=1),
        use_container_width=True,
        hide_index=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — WEALTH TRAJECTORY (INFLATION ADJUSTED)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-title">📈 Step 5 — Wealth Trajectory: Stagnant vs Reallocated (Inflation-Adjusted)</div>',
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="callout-amber">
    <b style='color:#92400e;'>⚠️ Inflation Reality Check:</b>
    <span style='color:#92400e;'>
    All values below are shown in <b>today's rupees</b> (inflation-adjusted at {inflation_rate:.1f}% p.a.).
    This shows real purchasing power — not just nominal numbers.
    </span>
</div>
""", unsafe_allow_html=True)

fig_wt = go.Figure()

fig_wt.add_trace(go.Scatter(
    x=years, y=stagnant_path,
    mode="lines+markers",
    name="Stagnant Asset (holding on)",
    line=dict(color="#dc2626", width=3, dash="dash"),
    marker=dict(size=6),
    hovertemplate="Year %{x}<br>Real Value: ₹%{y:,.0f}<extra></extra>"
))

fig_wt.add_trace(go.Scatter(
    x=years, y=reallocated_path,
    mode="lines+markers",
    name="Amaara Grove (reallocated)",
    line=dict(color="#16a34a", width=3),
    marker=dict(size=6),
    hovertemplate="Year %{x}<br>Real Value: ₹%{y:,.0f}<extra></extra>"
))

fig_wt.add_vline(
    x=total_years_recovery,
    line_dash="dot", line_color="#2563eb", line_width=2,
    annotation_text=f"Full Recovery\n(Yr {total_years_recovery})",
    annotation_position="top right",
    annotation_font_color="#2563eb"
)

fig_wt.update_layout(
    xaxis=dict(title="Year", dtick=1),
    yaxis=dict(title="Inflation-Adjusted Value (INR)", tickformat=",.0f"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=40, r=40, t=60, b=40),
    hovermode="x unified",
    plot_bgcolor="#f9fafb",
    height=420
)
st.plotly_chart(fig_wt, use_container_width=True)

# Summary cards
w1, w2, w3 = st.columns(3)

with w1:
    st.markdown(f"""
    <div class="step-box step-box-red">
        <div class="step-label">Real Value if Asset Stays Stagnant</div>
        <div class="big-number big-number-red">₹ {final_stagnant/1e7:.2f} Cr</div>
        <div class="sub-note">After {horizon} years at {inflation_rate:.1f}% inflation +
        ₹{holding_cost:,.0f}/yr holding cost.<br>
        <b>Total real wealth decay: ₹{total_wealth_decay/1e5:.1f} L</b></div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown(f"""
    <div class="step-box step-box-green">
        <div class="step-label">Real Value if Reallocated to Amaara Grove</div>
        <div class="big-number big-number-green">₹ {final_reallocated/1e7:.2f} Cr</div>
        <div class="sub-note">After {horizon} years at {target_return:.1f}% annual return,
        inflation-adjusted at {inflation_rate:.1f}%.</div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown(f"""
    <div class="step-box step-box-blue">
        <div class="step-label">Opportunity Gap (Real Wealth Difference)</div>
        <div class="big-number big-number-blue">₹ {opp_gap/1e7:.2f} Cr</div>
        <div class="sub-note">How much MORE real wealth the investor
        builds by reallocating vs holding.<br>
        <b>The cost of staying put.</b></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — DEAL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-title">✅ Deal Summary — The Full Picture</div>',
    unsafe_allow_html=True
)

summary_data = {
    "Parameter": [
        "Investor's Original Purchase Price",
        "Current Market Value (Distressed)",
        "Exit Price Offered (Original + Premium)",
        "Exit Premium Amount",
        "Transaction Costs (Haircut)",
        "Net Capital Deployed into Amaara Grove",
        "Amaara Grove Total Project Value",
        "Investor's Stake in Project",
        "Quarterly Recovery Amount",
        "Quarters to Full Recovery",
        "Years to Full Recovery",
        "Annual Holding Cost (if stayed)",
        f"Real Wealth if Stagnant (Yr {horizon})",
        f"Real Wealth if Reallocated (Yr {horizon})",
        "Opportunity Gap (Real Wealth)"
    ],
    "Value": [
        f"₹ {orig_price/1e7:.2f} Cr",
        f"₹ {curr_value/1e7:.2f} Cr  ({loss_pct:.1f}% below cost)",
        f"₹ {gross_exit_price/1e7:.2f} Cr",
        f"₹ {(orig_price * ep)/1e5:.1f} L  (+{exit_premium_pct:.0f}%)",
        f"₹ {transaction_costs/1e5:.1f} L  ({haircut_pct:.1f}%)",
        f"₹ {net_capital_deployed/1e7:.2f} Cr",
        f"₹ {project_value/1e7:.1f} Cr",
        f"{investor_stake_pct:.1f}%",
        f"₹ {quarterly_payout_amount/1e5:.1f} L  ({quarterly_recovery_pct:.1f}% of ₹{project_value/1e7:.0f} Cr)",
        f"{quarters_to_full_recovery}",
        f"{total_years_recovery}",
        f"₹ {holding_cost:,.0f} / year",
        f"₹ {final_stagnant/1e7:.2f} Cr",
        f"₹ {final_reallocated/1e7:.2f} Cr",
        f"₹ {opp_gap/1e7:.2f} Cr  (in investor's favour)"
    ]
}

summary_df = pd.DataFrame(summary_data)

def highlight_summary(row):
    if "Opportunity Gap" in str(row["Parameter"]):
        return ["background-color: #dcfce7; color: black; font-weight: bold"] * len(row)
    if "Exit Price" in str(row["Parameter"]):
        return ["background-color: #eff6ff; color: black"] * len(row)
    if "Stagnant" in str(row["Parameter"]):
        return ["background-color: #fef2f2; color: black"] * len(row)
    return [""] * len(row)

st.dataframe(
    summary_df.style.apply(highlight_summary, axis=1),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:0.78rem;
            margin-top:32px; padding-top:16px; border-top:1px solid #e5e7eb;'>
    Amaara Grove — Capital Reallocation Analyzer &nbsp;|&nbsp;
    Built for internal advisory use &nbsp;|&nbsp;
    All projections are indicative and based on input assumptions
</div>
""", unsafe_allow_html=True)