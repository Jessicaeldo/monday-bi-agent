import streamlit as st
from monday_api import fetch_board_data, convert_to_dataframe
import pandas as pd
from datetime import datetime

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(page_title="Monday BI Agent", layout="wide")
st.title("🚀 Monday Business Intelligence Agent")

# -----------------------------------
# BOARD IDS (YOUR BOARDS)
# -----------------------------------

deals_board_id = 5026838717
workorders_board_id = 5026839253

# -----------------------------------
# FETCH DATA FROM MONDAY
# -----------------------------------

# -----------------------------------
# FETCH DATA (CACHED)
# -----------------------------------

@st.cache_data(ttl=300)
def load_data():
    deals = convert_to_dataframe(fetch_board_data(deals_board_id))
    workorders = convert_to_dataframe(fetch_board_data(workorders_board_id))
    return deals, workorders

deals_df, workorders_df = load_data()

# -----------------------------------
# CLEAN DATA
# -----------------------------------

deals_df = deals_df.rename(columns={
    "date4": "close_date",
    "numeric_mm0x46qa": "deal_value"
})

workorders_df = workorders_df.rename(columns={
    "date4": "due_date"
})

# Convert types safely
deals_df["close_date"] = pd.to_datetime(deals_df.get("close_date"), errors="coerce")
deals_df["deal_value"] = pd.to_numeric(deals_df.get("deal_value"), errors="coerce")
workorders_df["due_date"] = pd.to_datetime(workorders_df.get("due_date"), errors="coerce")

# Remove rows without status
deals_df = deals_df[deals_df["status"].notna()]
workorders_df = workorders_df[workorders_df["status"].notna()]

# -----------------------------------
# SIDEBAR – SYSTEM STATUS
# -----------------------------------

st.sidebar.title("📊 System Status")
st.sidebar.success("Connected to Monday.com")

st.sidebar.write("Boards Loaded:")
st.sidebar.write(f"Deals: {len(deals_df)} rows")
st.sidebar.write(f"Work Orders: {len(workorders_df)} rows")

missing_deal_values = deals_df["deal_value"].isna().sum()
missing_dates = deals_df["close_date"].isna().sum()

st.sidebar.title("📋 Data Quality")
st.sidebar.write(f"Missing Deal Values: {missing_deal_values}")
st.sidebar.write(f"Missing Close Dates: {missing_dates}")

# -----------------------------------
# BUSINESS LOGIC FUNCTIONS
# -----------------------------------

def get_pipeline_summary():
    open_pipeline = deals_df[deals_df["status"] == "Open"]["deal_value"].sum()
    won_revenue = deals_df[deals_df["status"] == "Won"]["deal_value"].sum()
    total_pipeline = deals_df["deal_value"].sum()
    avg_deal_size = deals_df["deal_value"].mean()

    health_comment = "strong" if open_pipeline > avg_deal_size * 20 else "moderate"

    return f"""
📊 Pipeline Overview:

• Open Pipeline Value: ₹{open_pipeline:,.0f}
• Total Won Revenue: ₹{won_revenue:,.0f}
• Average Deal Size: ₹{avg_deal_size:,.0f}

Pipeline health appears {health_comment} based on current deal distribution.
"""


def get_win_rate_summary():
    closed = deals_df[deals_df["status"].isin(["Won", "Dead"])]

    if len(closed) == 0:
        return "No sufficient closed deal data available to calculate win rate."

    win_rate = (closed["status"] == "Won").mean() * 100

    if pd.isna(win_rate):
        return "Win rate cannot be calculated due to incomplete data."

    return f"""
🎯 Sales Performance:

• Win Rate: {win_rate:.2f}%

Conversion efficiency appears stable based on available records.
"""


def get_operations_summary():
    completed = len(workorders_df[workorders_df["status"] == "Done"])
    in_progress = len(workorders_df[workorders_df["status"] == "Working on it"])
    on_hold = len(workorders_df[workorders_df["status"] == "On Hold"])

    return f"""
⚙️ Operational Status:

• Completed Projects: {completed}
• Projects In Progress: {in_progress}
• Projects On Hold: {on_hold}

Operational load appears manageable at current execution capacity.
"""


def get_leadership_update():
    open_pipeline = deals_df[deals_df["status"] == "Open"]["deal_value"].sum()
    closed = deals_df[deals_df["status"].isin(["Won", "Dead"])]
    win_rate = (closed["status"] == "Won").mean() * 100 if len(closed) > 0 else 0

    return f"""
📈 Leadership Snapshot:

• Open Pipeline: ₹{open_pipeline:,.0f}
• Win Rate: {win_rate:.2f}%
• Active Projects: {len(workorders_df)}

Overall business momentum appears stable with strong revenue coverage.
"""

# -----------------------------------
# CHAT INTERFACE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a business question..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    if "pipeline" in q:
        response = get_pipeline_summary()

    elif "win rate" in q or "conversion" in q:
        response = get_win_rate_summary()

    elif "project" in q or "operations" in q:
        response = get_operations_summary()

    elif "leadership" in q or "summary" in q:
        response = get_leadership_update()

    else:
        response = "I’m not fully sure how to answer that yet. Try asking about pipeline health, win rate, operations, or leadership summary."

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)