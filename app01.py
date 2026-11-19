import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Telkom Indonesia | Subsidiary Financial & Risk Monitor (2025)",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cleaner metric cards and spacing
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. MOCK DATA GENERATION (2024 vs 2025 Annual Report Context)
# -----------------------------------------------------------------------------
@st.cache_data
def load_subsidiary_data() -> pd.DataFrame:
    """
    Generates realistic financial & risk data for PT Telkom Indonesia's
    major subsidiaries (values in IDR Billions).
    """
    data = [
        {
            "Subsidiary": "PT Telekomunikasi Selular (Telkomsel)",
            "Short_Name": "Telkomsel",
            "Sector": "Mobile & Digital Connectivity",
            "Revenue_2024": 86200.0,
            "Revenue_2025": 88500.0,
            "Net_Profit_2024": 15800.0,
            "Net_Profit_2025": 16200.0,
            "DSCR_2025": 3.10,
            "Operational_Context": (
                "Market leader in mobile telecommunications with strong FMC (Fixed-Mobile Convergence) "
                "synergies following IndiHome integration. Stable ARPU and growing digital services."
            ),
            "Key_Cost_Drivers": "Network operations & maintenance, spectrum fees, 5G capex depreciation.",
            "Risk_Mitigation_Status": (
                "Healthy balance sheet and strong operating cash flow. No covenant concerns; "
                "focusing on capex efficiency and digital monetization."
            ),
            "Special_Note": None
        },
        {
            "Subsidiary": "PT Dayamitra Telekomunikasi Tbk (Mitratel)",
            "Short_Name": "Mitratel",
            "Sector": "Telecommunication Infrastructure (Towers)",
            "Revenue_2024": 8750.0,
            "Revenue_2025": 9200.0,
            "Net_Profit_2024": 1950.0,
            "Net_Profit_2025": 2100.0,
            "DSCR_2025": 2.40,
            "Operational_Context": (
                "Largest towerco in Southeast Asia with steady tenancy ratio growth and "
                "fiber-to-the-tower (FTTT) expansion across Indonesia."
            ),
            "Key_Cost_Drivers": "Tower land leases, debt interest for inorganic acquisitions, maintenance.",
            "Risk_Mitigation_Status": (
                "Healthy debt profile with long-term locked-in tenant contracts providing "
                "predictable recurring cash flows."
            ),
            "Special_Note": None
        },
        {
            "Subsidiary": "PT Telkom Telekomunikasi Indonesia (Telkom Infra)",
            "Short_Name": "Telkom Infra",
            "Sector": "Wholesale & Network Infrastructure",
            "Revenue_2024": 3300.0,
            "Revenue_2025": 3500.0,
            "Net_Profit_2024": 165.0,
            "Net_Profit_2025": 180.0,
            "DSCR_2025": 1.60,
            "Operational_Context": (
                "Manages Telkom Group's backbone fiber optic, submarine cables, and "
                "network infrastructure assets."
            ),
            "Key_Cost_Drivers": "Submarine cable maintenance, power & energy costs, depreciation.",
            "Risk_Mitigation_Status": (
                "Healthy DSCR (1.6x). Ongoing asset utilization optimization and "
                "energy efficiency initiatives."
            ),
            "Special_Note": None
        },
        {
            "Subsidiary": "PT Telkom Satelit Indonesia (Telkomsat)",
            "Short_Name": "Telkomsat",
            "Sector": "Satellite & Maritime Connectivity",
            "Revenue_2024": 1250.0,
            "Revenue_2025": 1200.0,
            "Net_Profit_2024": -110.0,
            "Net_Profit_2025": -249.5,
            "DSCR_2025": 1.10,
            "Operational_Context": (
                "Provides satellite connectivity (Merah Putih 2 / HTS) for remote/3T areas, "
                "maritime, and enterprise backhaul."
            ),
            "Key_Cost_Drivers": (
                "Intense satellite market competition (LEO/Starlink), heavy satellite depreciation, "
                "and elevated interest expenses."
            ),
            "Risk_Mitigation_Status": (
                "DSCR at 1.10x (Warning zone: 1.0x - 1.25x). Focusing on B2B/government enterprise "
                "contracts and debt refinancing to ease interest burden."
            ),
            "Special_Note": (
                "Margin Pressure Alert: Telkomsat recorded a 2025 Net Loss of -Rp249.5B driven by "
                "satellite market competition, high depreciation, and interest expenses."
            )
        },
        {
            "Subsidiary": "PT Sigma Cipta Caraka (Sigma)",
            "Short_Name": "Sigma",
            "Sector": "IT Services, Data Center & Cloud",
            "Revenue_2024": 2250.0,
            "Revenue_2025": 2100.0,
            "Net_Profit_2024": -221.3,
            "Net_Profit_2025": -363.6,
            "DSCR_2025": 0.95,
            "Operational_Context": (
                "Enterprise IT solutions, system integration, and cloud services provider "
                "undergoing structural business transformation."
            ),
            "Key_Cost_Drivers": (
                "Clean Sheet Strategy implementation costs, legacy project write-offs, "
                "and high operational overhead."
            ),
            "Risk_Mitigation_Status": (
                "DSCR at 0.95x (Covenant Breach < 1.0x). Active engagement with lenders; "
                "BNI Loan Waiver required and currently in progress alongside cost restructuring."
            ),
            "Special_Note": (
                "Covenant Breach Alert: Sigma's 2025 Net Loss widened 64.3% YoY to -Rp363.6B due to "
                "Clean Sheet Strategy implementation. DSCR fell to 0.95x — BNI Loan Waiver Required."
            )
        }
    ]

    df = pd.DataFrame(data)

    # Derived Metrics
    df["Profit_Margin_2024_%"] = (df["Net_Profit_2024"] / df["Revenue_2024"]) * 100
    df["Profit_Margin_2025_%"] = (df["Net_Profit_2025"] / df["Revenue_2025"]) * 100
    df["Revenue_YoY_%"] = ((df["Revenue_2025"] - df["Revenue_2024"]) / df["Revenue_2024"]) * 100

    # Risk Categorization based on DSCR
    def classify_risk(dscr: float) -> str:
        if dscr < 1.0:
            return "High Risk / Covenant Breach"
        elif dscr <= 1.25:
            return "Warning"
        else:
            return "Healthy"

    df["Risk_Category"] = df["DSCR_2025"].apply(classify_risk)
    return df


df_raw = load_subsidiary_data()


# Helper function to format IDR Billions into readable Trillions / Billions
def format_idr(val_billions: float) -> str:
    abs_val = abs(val_billions)
    sign = "-" if val_billions < 0 else ""
    if abs_val >= 1000:
        return f"{sign}Rp{abs_val / 1000:,.2f}T"
    return f"{sign}Rp{abs_val:,.1f}B"


# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.title("📡 Telkom Group Monitor")
st.sidebar.caption("2025 Annual Report Context")
st.sidebar.divider()

# Subsidiary Multiselect
all_subs = df_raw["Short_Name"].tolist()
selected_subs = st.sidebar.multiselect(
    "Select Subsidiaries",
    options=all_subs,
    default=all_subs
)

# Risk Category Filter
risk_options = ["All", "High Risk / Covenant Breach", "Warning", "Healthy"]
selected_risk = st.sidebar.selectbox(
    "Filter by Risk Category",
    options=risk_options,
    index=0
)

# View Mode Toggle
view_mode = st.sidebar.radio(
    "View Mode",
    options=["2024/2025 YoY Comparison", "2025 Overview"],
    index=0
)

st.sidebar.divider()
st.sidebar.info(
    "**DSCR Thresholds:**\n"
    "- 🔴 **< 1.00x**: Covenant Breach\n"
    "- 🟡 **1.00x – 1.25x**: Warning\n"
    "- 🟢 **> 1.25x**: Healthy"
)

# Apply Filters
df_filtered = df_raw[df_raw["Short_Name"].isin(selected_subs)].copy()
if selected_risk != "All":
    df_filtered = df_filtered[df_filtered["Risk_Category"] == selected_risk]

if df_filtered.empty:
    st.warning("No subsidiaries match the selected filters. Please adjust your sidebar selection.")
    st.stop()


# -----------------------------------------------------------------------------
# 4. HEADER & KPI METRICS (TOP BANNER)
# -----------------------------------------------------------------------------
st.title("PT Telkom Indonesia — Subsidiary Performance & Financial Risk Dashboard")
st.markdown("Monitoring subsidiary revenue, profitability, and debt covenant compliance (2024 vs 2025).")

# Calculate Consolidated KPIs
tot_rev_2025 = df_filtered["Revenue_2025"].sum()
tot_rev_2024 = df_filtered["Revenue_2024"].sum()
rev_yoy_pct = ((tot_rev_2025 - tot_rev_2024) / tot_rev_2024) * 100 if tot_rev_2024 else 0.0

tot_profit_2025 = df_filtered["Net_Profit_2025"].sum()
tot_profit_2024 = df_filtered["Net_Profit_2024"].sum()
profit_yoy_pct = ((tot_profit_2025 - tot_profit_2024) / abs(tot_profit_2024)) * 100 if tot_profit_2024 else 0.0

high_risk_count = (df_filtered["DSCR_2025"] < 1.0).sum()
warning_count = ((df_filtered["DSCR_2025"] >= 1.0) & (df_filtered["DSCR_2025"] <= 1.25)).sum()

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        label="Consolidated Subsidiary Revenue (2025)",
        value=format_idr(tot_rev_2025),
        delta=f"{rev_yoy_pct:+.2f}% YoY"
    )

with kpi2:
    st.metric(
        label="Total Net Profit / Loss (2025)",
        value=format_idr(tot_profit_2025),
        delta=f"{profit_yoy_pct:+.2f}% YoY"
    )

with kpi3:
    st.metric(
        label="High Risk / Breached Covenant Alerts",
        value=f"{high_risk_count} Breached",
        delta=f"{warning_count} Warning" if warning_count > 0 else "0 Warning",
        delta_color="inverse"
    )

st.divider()


# -----------------------------------------------------------------------------
# 5. MAIN TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Financial Health & Performance",
    "⚠️ Debt Covenant & Risk Alert System",
    "🔍 Subsidiary Drill-Down Analysis"
])


# =============================================================================
# TAB 1: FINANCIAL HEALTH & PERFORMANCE OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Revenue & Net Profit Performance")

    col_chart1, col_chart2 = st.columns(2)

    # Chart 1: Revenue Comparison (Neutral Blue palette)
    with col_chart1:
        if view_mode == "2024/2025 YoY Comparison":
            rev_melted = df_filtered.melt(
                id_vars=["Short_Name"],
                value_vars=["Revenue_2024", "Revenue_2025"],
                var_name="Year",
                value_name="Revenue_B"
            )
            rev_melted["Year"] = rev_melted["Year"].str.replace("Revenue_", "")
            fig_rev = px.bar(
                rev_melted,
                x="Short_Name",
                y="Revenue_B",
                color="Year",
                barmode="group",
                title="Revenue: 2024 vs 2025 (IDR Billions)",
                color_discrete_map={"2024": "#93C5FD", "2025": "#1D4ED8"},
                labels={"Short_Name": "Subsidiary", "Revenue_B": "Revenue (Rp Billions)"}
            )
        else:
            fig_rev = px.bar(
                df_filtered,
                x="Short_Name",
                y="Revenue_2025",
                title="2025 Revenue by Subsidiary (IDR Billions)",
                color_discrete_sequence=["#1D4ED8"],
                labels={"Short_Name": "Subsidiary", "Revenue_2025": "Revenue (Rp Billions)"}
            )
        fig_rev.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_rev, use_container_width=True)

    # Chart 2: Net Profit/Loss Comparison (Green for Profit, Red for Loss)
    with col_chart2:
        if view_mode == "2024/2025 YoY Comparison":
            prof_melted = df_filtered.melt(
                id_vars=["Short_Name"],
                value_vars=["Net_Profit_2024", "Net_Profit_2025"],
                var_name="Year",
                value_name="Net_Profit_B"
            )
            prof_melted["Year"] = prof_melted["Year"].str.replace("Net_Profit_", "")
            fig_prof = px.bar(
                prof_melted,
                x="Short_Name",
                y="Net_Profit_B",
                color="Year",
                barmode="group",
                title="Net Profit / Loss: 2024 vs 2025 (IDR Billions)",
                color_discrete_map={"2024": "#86EFAC", "2025": "#15803D"},
                labels={"Short_Name": "Subsidiary", "Net_Profit_B": "Net Profit/Loss (Rp Billions)"}
            )
        else:
            df_filtered["Profit_Status"] = df_filtered["Net_Profit_2025"].apply(
                lambda x: "Profit" if x >= 0 else "Loss"
            )
            fig_prof = px.bar(
                df_filtered,
                x="Short_Name",
                y="Net_Profit_2025",
                color="Profit_Status",
                title="2025 Net Profit / Loss by Subsidiary (IDR Billions)",
                color_discrete_map={"Profit": "#16A34A", "Loss": "#DC2626"},
                labels={"Short_Name": "Subsidiary", "Net_Profit_2025": "Net Profit/Loss (Rp Billions)"}
            )
        fig_prof.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_prof.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_prof, use_container_width=True)

    # Summary Table with Conditional Formatting
    st.subheader("Subsidiary Financial Summary Table")
    table_df = df_filtered[[
        "Subsidiary", "Revenue_2024", "Revenue_2025", "Revenue_YoY_%",
        "Net_Profit_2024", "Net_Profit_2025", "Profit_Margin_2025_%", "DSCR_2025", "Risk_Category"
    ]].copy()

    table_df.columns = [
        "Subsidiary", "2024 Rev (RpB)", "2025 Rev (RpB)", "Rev YoY (%)",
        "2024 Net Profit (RpB)", "2025 Net Profit (RpB)", "2025 Margin (%)", "DSCR (x)", "Risk Status"
    ]

    def color_margin(val):
        if val < 0:
            return "background-color: #FEE2E2; color: #991B1B; font-weight: bold;"
        elif val < 10:
            return "background-color: #FEF3C7; color: #92400E;"
        return "background-color: #DCFCE7; color: #166534; font-weight: bold;"

    styled_table = (
        table_df.style
        .format({
            "2024 Rev (RpB)": "{:,.1f}",
            "2025 Rev (RpB)": "{:,.1f}",
            "Rev YoY (%)": "{:+.2f}%",
            "2024 Net Profit (RpB)": "{:,.1f}",
            "2025 Net Profit (RpB)": "{:,.1f}",
            "2025 Margin (%)": "{:+.2f}%",
            "DSCR (x)": "{:.2f}x"
        })
        .map(color_margin, subset=["2025 Margin (%)"])
    )

    st.dataframe(styled_table, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 2: DEBT COVENANT & RISK ALERT SYSTEM
# =============================================================================
with tab2:
    st.subheader("Debt Service Coverage Ratio (DSCR) & Covenant Monitoring")
    st.caption("Covenant Thresholds: < 1.00x (Breach) | 1.00x - 1.25x (Warning) | > 1.25x (Healthy)")

    # DSCR Gauge Charts
    gauge_cols = st.columns(len(df_filtered))
    for idx, (_, row) in enumerate(df_filtered.iterrows()):
        dscr_val = row["DSCR_2025"]
        bar_color = "#DC2626" if dscr_val < 1.0 else ("#D97706" if dscr_val <= 1.25 else "#16A34A")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=dscr_val,
            number={"suffix": "x", "font": {"size": 24}},
            title={"text": row["Short_Name"], "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 3.5], "tickwidth": 1},
                "bar": {"color": bar_color},
                "steps": [
                    {"range": [0, 1.0], "color": "#FEE2E2"},
                    {"range": [1.0, 1.25], "color": "#FEF3C7"},
                    {"range": [1.25, 3.5], "color": "#DCFCE7"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.75,
                    "value": 1.0
                }
            }
        ))
        fig_gauge.update_layout(height=230, margin=dict(l=15, r=15, t=40, b=10))
        with gauge_cols[idx]:
            st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()
    st.subheader("Automated Risk & Covenant Alert Cards")

    # Visual Alert Cards
    for _, row in df_filtered.sort_values("DSCR_2025").iterrows():
        dscr = row["DSCR_2025"]
        name = row["Subsidiary"]
        net_prof_str = format_idr(row["Net_Profit_2025"])

        if dscr < 1.0:
            st.error(
                f"🚨 **COVENANT BREACH — {name}** | DSCR: **{dscr:.2f}x** (< 1.00x) | "
                f"2025 Net Loss: **{net_prof_str}**\n\n"
                f"**Action Required:** {row['Special_Note'] or row['Risk_Mitigation_Status']}"
            )
        elif dscr <= 1.25:
            st.warning(
                f"⚠️ **WARNING — {name}** | DSCR: **{dscr:.2f}x** (1.00x – 1.25x) | "
                f"2025 Net Loss: **{net_prof_str}**\n\n"
                f"**Context:** {row['Special_Note'] or row['Risk_Mitigation_Status']}"
            )
        else:
            st.success(
                f"✅ **HEALTHY — {name}** | DSCR: **{dscr:.2f}x** (> 1.25x) | "
                f"2025 Net Profit: **{net_prof_str}** — Compliant with all debt covenants."
            )


# =============================================================================
# TAB 3: SUBSIDIARY DRILL-DOWN ANALYSIS
# =============================================================================
with tab3:
    st.subheader("Detailed Subsidiary Profile & Risk Mitigation")

    selected_sub_detail = st.selectbox(
        "Choose a Subsidiary to Examine",
        options=df_filtered["Subsidiary"].tolist()
    )

    sub_row = df_filtered[df_filtered["Subsidiary"] == selected_sub_detail].iloc[0]

    # Top-level metrics for selected subsidiary
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("2025 Revenue", format_idr(sub_row["Revenue_2025"]), f"{sub_row['Revenue_YoY_%']:+.2f}% YoY")
    m2.metric("2025 Net Profit/Loss", format_idr(sub_row["Net_Profit_2025"]))
    m3.metric("2025 Profit Margin", f"{sub_row['Profit_Margin_2025_%']:+.2f}%")
    m4.metric("DSCR (2025)", f"{sub_row['DSCR_2025']:.2f}x", sub_row["Risk_Category"])

    st.divider()

    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        st.markdown(f"**Sector:** {sub_row['Sector']}")
        st.markdown("#### Operational Context")
        st.info(sub_row["Operational_Context"])

        st.markdown("#### Key Cost Drivers")
        st.write(sub_row["Key_Cost_Drivers"])

        st.markdown("#### Risk Mitigation & Covenant Status")
        if sub_row["DSCR_2025"] < 1.0:
            st.error(sub_row["Risk_Mitigation_Status"])
        elif sub_row["DSCR_2025"] <= 1.25:
            st.warning(sub_row["Risk_Mitigation_Status"])
        else:
            st.success(sub_row["Risk_Mitigation_Status"])

    with c_right:
        # Mini YoY comparison chart for the selected subsidiary
        comp_df = pd.DataFrame({
            "Metric": ["Revenue", "Revenue", "Net Profit/Loss", "Net Profit/Loss"],
            "Year": ["2024", "2025", "2024", "2025"],
            "Amount (RpB)": [
                sub_row["Revenue_2024"],
                sub_row["Revenue_2025"],
                sub_row["Net_Profit_2024"],
                sub_row["Net_Profit_2025"]
            ]
        })
        fig_sub = px.bar(
            comp_df,
            x="Metric",
            y="Amount (RpB)",
            color="Year",
            barmode="group",
            title=f"{sub_row['Short_Name']} — 2024 vs 2025 Financial Snapshot",
            color_discrete_map={"2024": "#94A3B8", "2025": "#2563EB"}
        )
        fig_sub.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_sub, use_container_width=True)
