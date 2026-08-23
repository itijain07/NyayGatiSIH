import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

# ============================================================
# NYAYGATI - Simple SIH Prototype
# Predict -> Analyze -> Optimize
# All figures in this prototype are DEMO/SIMULATED.
# ============================================================

st.set_page_config(
    page_title="NyayGati",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- Styling ---------------------------
st.markdown("""
<style>
    .main { background-color: #f7f9fc; }
    .block-container { padding-top: 2rem; }
    .hero {
        padding: 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #0b3d91, #1769aa);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 { margin: 0; font-size: 3rem; }
    .hero p { font-size: 1.1rem; margin-top: .5rem; }
    .module-card {
        padding: 1.4rem;
        border: 1px solid #dce3ec;
        border-radius: 14px;
        background: white;
        min-height: 180px;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
    }
    .metric-card {
        padding: 1rem;
        border: 1px solid #dce3ec;
        border-radius: 12px;
        background: white;
    }
    .demo {
        background: #fff7df;
        border-left: 5px solid #e0a800;
        padding: .8rem 1rem;
        border-radius: 6px;
        margin: .8rem 0 1.2rem;
    }
    .disclaimer {
        background: #eef4fb;
        border-left: 5px solid #1769aa;
        padding: .8rem 1rem;
        border-radius: 6px;
    }
    .small-muted { color: #64748b; font-size: .9rem; }
</style>
""", unsafe_allow_html=True)

COURTS = ["Saket District Court", "Patiala House Court", "Rohini District Court"]
CASE_TYPES = ["Cheque Bounce", "Property Dispute", "Motor Accident Claim"]

# ---------------------- DEMO DATA ----------------------------
prediction_data = {
    ("Saket District Court", "Cheque Bounce"): (9, 15, 22),
    ("Saket District Court", "Property Dispute"): (14, 24, 36),
    ("Saket District Court", "Motor Accident Claim"): (12, 20, 30),
    ("Patiala House Court", "Cheque Bounce"): (8, 14, 21),
    ("Patiala House Court", "Property Dispute"): (13, 22, 34),
    ("Patiala House Court", "Motor Accident Claim"): (11, 19, 28),
    ("Rohini District Court", "Cheque Bounce"): (10, 17, 25),
    ("Rohini District Court", "Property Dispute"): (15, 26, 38),
    ("Rohini District Court", "Motor Accident Claim"): (13, 21, 31),
}

analytics_data = {
    ("Saket District Court", "Cheque Bounce"): {
        "pending": 3400, "disposed": 2850, "duration": 14,
        "hearings": 3, "gap": 45, "backlog": 54,
        "adjournment": 31,
    },
    ("Saket District Court", "Property Dispute"): {
        "pending": 2200, "disposed": 1800, "duration": 24,
        "hearings": 5, "gap": 62, "backlog": 55,
        "adjournment": 27,
    },
    ("Saket District Court", "Motor Accident Claim"): {
        "pending": 1800, "disposed": 1600, "duration": 20,
        "hearings": 4, "gap": 53, "backlog": 53,
        "adjournment": 24,
    },
    ("Patiala House Court", "Cheque Bounce"): {
        "pending": 2700, "disposed": 2500, "duration": 13,
        "hearings": 3, "gap": 41, "backlog": 52,
        "adjournment": 28,
    },
    ("Patiala House Court", "Property Dispute"): {
        "pending": 1900, "disposed": 1700, "duration": 21,
        "hearings": 5, "gap": 58, "backlog": 53,
        "adjournment": 25,
    },
    ("Patiala House Court", "Motor Accident Claim"): {
        "pending": 1500, "disposed": 1450, "duration": 18,
        "hearings": 4, "gap": 49, "backlog": 51,
        "adjournment": 22,
    },
    ("Rohini District Court", "Cheque Bounce"): {
        "pending": 3100, "disposed": 2600, "duration": 15,
        "hearings": 3, "gap": 48, "backlog": 54,
        "adjournment": 30,
    },
    ("Rohini District Court", "Property Dispute"): {
        "pending": 2400, "disposed": 1950, "duration": 25,
        "hearings": 5, "gap": 65, "backlog": 55,
        "adjournment": 29,
    },
    ("Rohini District Court", "Motor Accident Claim"): {
        "pending": 1700, "disposed": 1500, "duration": 21,
        "hearings": 4, "gap": 55, "backlog": 53,
        "adjournment": 25,
    },
}

pending_cases = {
    "Saket District Court": [
        {"Case ID": "C001", "Case Type": "Cheque Bounce", "Case Age": 18, "Hearings": 2, "Priority": "Old"},
        {"Case ID": "C002", "Case Type": "Property Dispute", "Case Age": 8, "Hearings": 4, "Priority": "Normal"},
        {"Case ID": "C003", "Case Type": "Cheque Bounce", "Case Age": 24, "Hearings": 3, "Priority": "Very Old"},
        {"Case ID": "C004", "Case Type": "Motor Accident Claim", "Case Age": 13, "Hearings": 2, "Priority": "Old"},
        {"Case ID": "C005", "Case Type": "Property Dispute", "Case Age": 6, "Hearings": 2, "Priority": "Normal"},
        {"Case ID": "C006", "Case Type": "Cheque Bounce", "Case Age": 21, "Hearings": 1, "Priority": "Very Old"},
        {"Case ID": "C007", "Case Type": "Motor Accident Claim", "Case Age": 10, "Hearings": 3, "Priority": "Normal"},
    ],
    "Patiala House Court": [
        {"Case ID": "P001", "Case Type": "Cheque Bounce", "Case Age": 20, "Hearings": 2, "Priority": "Very Old"},
        {"Case ID": "P002", "Case Type": "Property Dispute", "Case Age": 9, "Hearings": 3, "Priority": "Normal"},
        {"Case ID": "P003", "Case Type": "Motor Accident Claim", "Case Age": 15, "Hearings": 2, "Priority": "Old"},
        {"Case ID": "P004", "Case Type": "Cheque Bounce", "Case Age": 7, "Hearings": 1, "Priority": "Normal"},
        {"Case ID": "P005", "Case Type": "Property Dispute", "Case Age": 23, "Hearings": 4, "Priority": "Very Old"},
    ],
    "Rohini District Court": [
        {"Case ID": "R001", "Case Type": "Cheque Bounce", "Case Age": 22, "Hearings": 2, "Priority": "Very Old"},
        {"Case ID": "R002", "Case Type": "Property Dispute", "Case Age": 11, "Hearings": 3, "Priority": "Old"},
        {"Case ID": "R003", "Case Type": "Motor Accident Claim", "Case Age": 7, "Hearings": 2, "Priority": "Normal"},
        {"Case ID": "R004", "Case Type": "Cheque Bounce", "Case Age": 17, "Hearings": 1, "Priority": "Old"},
        {"Case ID": "R005", "Case Type": "Property Dispute", "Case Age": 25, "Hearings": 5, "Priority": "Very Old"},
    ],
}

slots = {"Monday": 8, "Tuesday": 7, "Wednesday": 9, "Thursday": 6, "Friday": 8}


def chart(fig):
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def make_prediction_chart(p50, p75, p90):
    times = np.arange(1, max(p90 + 5, 25))
    # Simple illustrative cumulative curve through the three demo points.
    probs = np.interp(times, [p50, p75, p90], [50, 75, 90])
    probs = np.maximum.accumulate(probs)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(times, probs, linewidth=2)
    ax.scatter([p50, p75, p90], [50, 75, 90], s=55)
    ax.set_xlabel("Estimated duration (months)")
    ax.set_ylabel("Similar cases reached (%)")
    ax.set_ylim(0, 100)
    ax.grid(alpha=.2)
    fig.tight_layout()
    return fig


def analytics_charts(court, case_type):
    base = analytics_data[(court, "Cheque Bounce" if case_type == "All Cases" else case_type)]

    # Pending by case type
    vals = [analytics_data[(court, c)]["pending"] for c in CASE_TYPES]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(CASE_TYPES, vals)
    ax.set_ylabel("Pending cases (demo)")
    ax.set_title("Pending cases by case type")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    chart(fig)

    # Disposed over time
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    start = base["disposed"] - 650
    disposed = np.linspace(start, base["disposed"], 6).astype(int)
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(months, disposed, marker="o", linewidth=2)
    ax.set_ylabel("Disposed cases (demo)")
    ax.set_title("Cases disposed over time")
    ax.grid(alpha=.2)
    fig.tight_layout()
    chart(fig)

    # Age distribution
    ages = [6, 12, 18, 24, 30, 36]
    counts = [base["pending"] * x for x in [.30, .23, .18, .13, .09, .07]]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar([str(a) for a in ages], counts)
    ax.set_xlabel("Case age (months)")
    ax.set_ylabel("Number of cases (demo)")
    ax.set_title("Case age distribution")
    fig.tight_layout()
    chart(fig)

    # Hearing gap
    gaps = [base["gap"] + x for x in [-12, -6, 0, 5, 11]]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(["Q1", "Q2", "Q3", "Q4", "Q5"], gaps, marker="o", linewidth=2)
    ax.set_ylabel("Average gap (days)")
    ax.set_title("Average hearing gap trend")
    ax.grid(alpha=.2)
    fig.tight_layout()
    chart(fig)

    # Backlog trend
    backlog = [base["backlog"] + x for x in [5, 4, 3, 1, 0, -2]]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(months, backlog, marker="o", linewidth=2)
    ax.set_ylabel("Backlog (%)")
    ax.set_title("Backlog trend")
    ax.grid(alpha=.2)
    fig.tight_layout()
    chart(fig)


def generate_schedule(court):
    cases = sorted(
        pending_cases[court],
        key=lambda x: (-x["Case Age"], x["Hearings"])
    )

    day_list = list(slots.keys())
    schedule = []
    day_index = 0

    # Transparent demo rule:
    # 1. Older cases first.
    # 2. If ages are close, fewer hearings first.
    # 3. Fill available slots sequentially.
    for case in cases:
        placed = False
        for _ in range(len(day_list)):
            day = day_list[day_index % len(day_list)]
            used = sum(1 for x in schedule if x["Day"] == day)
            if used < slots[day]:
                reason = (
                    "Very old pending case"
                    if case["Case Age"] >= 20
                    else "Older pending case"
                    if case["Case Age"] >= 12
                    else "Fewer hearings / available slot"
                )
                schedule.append({
                    "Day": day,
                    "Case ID": case["Case ID"],
                    "Case Type": case["Case Type"],
                    "Case Age": f'{case["Case Age"]} months',
                    "Reason": reason,
                })
                day_index += 1
                placed = True
                break
            day_index += 1
        if not placed:
            break

    return pd.DataFrame(schedule)


# ------------------------- Sidebar ----------------------------
st.sidebar.markdown("## ⚖️ NYAYGATI")
st.sidebar.caption("Intelligent Judicial Case Management")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Case Duration Prediction", "Court + Case Analytics",
     "Intelligent Schedule Generator", "About NyayGati"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Prototype • Demo/Simulated Data")

# --------------------------- Home -----------------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>⚖️ NYAYGATI</h1>
        <p>Intelligent Judicial Case Management & Backlog Optimization</p>
        <p>Predict → Analyze → Optimize</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="demo">
    <b>DEMO PROTOTYPE:</b> All case figures, predictions and schedules shown here are
    simulated for demonstration and are not live court data or actual court decisions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### One platform. Three questions.")
    cols = st.columns(3)

    cards = [
        ("🔮", "Case Duration Prediction",
         "Estimate how long a case may take using predefined demo results based on similar historical cases."),
        ("🔍", "Court + Case Analytics",
         "Understand pending cases, delays, hearings, backlog and trends for a selected court and case type."),
        ("⚙️", "Intelligent Schedule Generator",
         "Generate a proposed schedule using pending-case data and available court resources."),
    ]

    for col, (icon, title, text) in zip(cols, cards):
        with col:
            st.markdown(f"""
            <div class="module-card">
                <h2>{icon} {title}</h2>
                <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### How NyayGati works")
    st.info("PREDICT  →  ANALYZE  →  OPTIMIZE")

    st.markdown("""
    <div class="disclaimer">
    <b>Important:</b> NyayGati is a decision-support prototype. Its predictions and
    proposed schedules are simulated and do not replace judicial decisions.
    </div>
    """, unsafe_allow_html=True)

# --------------------- Prediction ------------------------------
elif page == "Case Duration Prediction":
    st.title("🔮 Case Duration Prediction")
    st.caption("Estimate duration using simple predefined demo results for similar cases.")

    st.markdown("""
    <div class="demo"><b>DEMO DATA:</b> Prediction outputs are simulated.
    They are not guaranteed disposal dates and are not generated by a trained ML model.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        court = st.selectbox("Court", COURTS)
        case_type = st.selectbox("Case Type", CASE_TYPES)
        filing_date = st.date_input("Filing Date", value=date.today())
    with col2:
        status = st.selectbox("Current Status", ["Pending", "Recently Filed", "Ongoing"])
        hearings = st.number_input("Hearings completed (basic detail)", min_value=0, max_value=50, value=0)
        notes = st.text_input("Optional basic case detail", placeholder="e.g. number of parties / simple note")

    if st.button("Predict Case Duration", type="primary", use_container_width=True):
        p50, p75, p90 = prediction_data[(court, case_type)]

        st.markdown("## Estimated Case Duration")
        a, b, c = st.columns(3)
        a.metric("50% of similar cases", f"~{p50} months")
        b.metric("75% of similar cases", f"~{p75} months")
        c.metric("90% of similar cases", f"~{p90} months")

        st.caption(f"Selected: {case_type} • {court} • Status: {status}")
        st.markdown("### Probability / time relationship")
        chart(make_prediction_chart(p50, p75, p90))

        st.markdown("""
        <div class="disclaimer">
        <b>Important:</b> This is an estimate based on simulated similar-case data,
        not a guaranteed disposal date or judicial prediction.
        </div>
        """, unsafe_allow_html=True)

# ----------------------- Analytics -----------------------------
elif page == "Court + Case Analytics":
    st.title("🔍 Court + Case Analytics")
    st.caption("Explore simulated backlog and delay patterns for a selected court and case type.")

    st.markdown("""
    <div class="demo"><b>DEMO DATA:</b> All statistics and charts on this page are
    simulated for the prototype and should not be presented as actual court statistics.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        court = st.selectbox("Select Court", COURTS)
    with col2:
        case_type = st.selectbox("Select Case Type", CASE_TYPES + ["All Cases"])

    key_type = "Cheque Bounce" if case_type == "All Cases" else case_type
    d = analytics_data[(court, key_type)]

    st.markdown(f"### {court} — {case_type}")

    metric_cols = st.columns(6)
    metrics = [
        ("Total Pending Cases", f'{d["pending"]:,}'),
        ("Disposed Cases", f'{d["disposed"]:,}'),
        ("Avg. Case Duration", f'{d["duration"]} months'),
        ("Avg. Hearings / Case", str(d["hearings"])),
        ("Avg. Hearing Gap", f'{d["gap"]} days'),
        ("Backlog", f'{d["backlog"]}%'),
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="small-muted">{label}</div>
                <h3>{value}</h3>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Delay & backlog patterns")
    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.metric("Adjournment pattern", f'{d["adjournment"]}%')
        st.caption("Share shown here is simulated for demonstration.")
    with chart_cols[1]:
        st.metric("Pending trend", "Increasing" if d["backlog"] >= 54 else "Stable / decreasing")
        st.caption("Trend is simulated from prototype data.")

    analytics_charts(court, case_type)

    st.markdown("### Potential Bottlenecks")
    bottlenecks = [
        f"High number of pending {case_type.lower()} cases.",
        f"Average hearing gap of {d['gap']} days may contribute to delay.",
        "Older pending cases require focused administrative attention.",
        "Adjournment patterns can increase the time required to clear the backlog.",
    ]
    for item in bottlenecks:
        st.warning(item)

# --------------------- Schedule Generator ---------------------
elif page == "Intelligent Schedule Generator":
    st.title("⚙️ Intelligent Schedule Generator")
    st.caption("Generate a proposed schedule for administrative review.")

    st.markdown("""
    <div class="demo"><b>DEMO SIMULATION:</b> The cases, slots, clearance estimates and
    proposed schedule are simulated. The scheduling logic is deliberately simple and transparent.</div>
    """, unsafe_allow_html=True)

    court = st.selectbox("Select Court", COURTS)

    st.markdown("### Pending Cases")
    cases_df = pd.DataFrame(pending_cases[court])
    st.dataframe(cases_df, use_container_width=True, hide_index=True)

    st.markdown("### Available Hearing Slots")
    slot_df = pd.DataFrame({
        "Day": list(slots.keys()),
        "Available Slots": list(slots.values())
    })
    st.dataframe(slot_df, use_container_width=True, hide_index=True)

    st.markdown("### Scheduling Logic")
    st.write("""
    1. Older pending cases are considered first.
    2. Where ages are similar, cases with fewer completed hearings are considered earlier.
    3. Available slots are filled without exceeding the defined daily capacity.
    4. The result is a proposed schedule for administrative review.
    """)

    if st.button("Generate Optimized Schedule", type="primary", use_container_width=True):
        schedule_df = generate_schedule(court)

        st.markdown("## Schedule Comparison")
        a, b, c = st.columns(3)
        a.metric("Current projected clearance", "14 months")
        b.metric("NyayGati proposed schedule", "10 months")
        c.metric("Projected improvement", "~4 months")

        st.markdown("## NYAYGATI Proposed Schedule")
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)

        st.markdown("### Current Schedule vs Proposed Schedule")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(["Current", "NyayGati Proposed"], [14, 10])
        ax.set_ylabel("Projected clearance (months)")
        ax.set_title("Projected clearance comparison")
        fig.tight_layout()
        chart(fig)

        st.markdown("""
        <div class="disclaimer">
        <b>Administrative simulation only:</b> NyayGati does not automatically modify
        real court schedules and does not decide which cases judges should hear.
        The final scheduling decision remains with the court administration/judiciary.
        </div>
        """, unsafe_allow_html=True)

# -------------------------- About ------------------------------
else:
    st.title("ℹ️ About NyayGati")

    st.markdown("""
    ### Problem

    Courts handle large numbers of pending cases and delays. Citizens may not have
    a simple way to understand the approximate duration of a case, while court
    administration needs better visibility into backlog and delay patterns.

    ### Solution

    **NyayGati** is a judicial decision-support prototype built around three connected ideas:

    **1. Predict** — estimate approximate case duration using similar historical/demo cases.

    **2. Analyze** — show court + case-type analytics such as pending cases, disposed cases,
    hearing gaps, backlog, adjournments and trends.

    **3. Optimize** — simulate a proposed schedule using pending-case information and
    available court resources.

    ### Data

    This prototype uses **simulated/demo data**. It does not use live court records or
    claim that the displayed statistics are actual Saket, Patiala House or Rohini court data.

    A future system could integrate authorized/public sources such as **NJDG and e-Courts**,
    subject to data availability, permissions and access.

    ### Technology

    - Python
    - Streamlit
    - Pandas
    - NumPy
    - Matplotlib

    ### Prototype scope

    The prediction module uses predefined demo outputs instead of a complicated machine
    learning model. The schedule generator uses a simple rule-based simulation so that
    the logic is transparent and easy to explain.

    ### Core idea

    **PREDICT → ANALYZE → OPTIMIZE**

    NyayGati is intended to support administrative understanding and simulation.
    It does not replace judicial decisions.
    """)

    st.markdown("""
    <div class="disclaimer">
    <b>Prototype disclaimer:</b> Predictions and proposed schedules shown by NyayGati
    are simulated and should not be treated as actual court decisions, guaranteed
    disposal dates, or live court statistics.
    </div>
    """, unsafe_allow_html=True)
