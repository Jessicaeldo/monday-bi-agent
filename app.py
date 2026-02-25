from monday_api import fetch_board_data, convert_to_dataframe
import pandas as pd
from datetime import datetime

# -----------------------------------
# BOARD IDS
# -----------------------------------

deals_board_id = 5026838717
workorders_board_id = 5026839253

# -----------------------------------
# FETCH DATA
# -----------------------------------

deals_df = convert_to_dataframe(fetch_board_data(deals_board_id))
workorders_df = convert_to_dataframe(fetch_board_data(workorders_board_id))

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

deals_df["close_date"] = pd.to_datetime(deals_df["close_date"], errors="coerce")
deals_df["deal_value"] = pd.to_numeric(deals_df["deal_value"], errors="coerce")
workorders_df["due_date"] = pd.to_datetime(workorders_df["due_date"], errors="coerce")

deals_df = deals_df[deals_df["status"].notna()]
workorders_df = workorders_df[workorders_df["status"].notna()]

# -----------------------------------
# BUSINESS METRICS FUNCTIONS
# -----------------------------------

def get_pipeline_summary():
    open_pipeline = deals_df[deals_df["status"] == "Open"]["deal_value"].sum()
    return f"Open pipeline value is {open_pipeline:,.0f}"

def get_win_rate():
    closed = deals_df[deals_df["status"].isin(["Won", "Dead"])]
    if len(closed) == 0:
        return "No closed deals available."
    win_rate = (closed["status"] == "Won").mean() * 100
    return f"Win rate is {win_rate:.2f}%"

def get_operations_summary():
    completed = len(workorders_df[workorders_df["status"] == "Done"])
    in_progress = len(workorders_df[workorders_df["status"] == "Working on it"])
    return f"We have {completed} completed projects and {in_progress} projects currently in progress."

# -----------------------------------
# SIMPLE AGENT
# -----------------------------------

print("\n=== Monday Business Intelligence Agent ===")
print("Ask a business question (type 'exit' to quit)\n")

while True:
    query = input("Founder: ").lower()

    if query == "exit":
        break

    if "pipeline" in query:
        print("Agent:", get_pipeline_summary())

    elif "win rate" in query:
        print("Agent:", get_win_rate())

    elif "project" in query or "operations" in query:
        print("Agent:", get_operations_summary())

    else:
        print("Agent: I'm not sure. Try asking about pipeline, win rate, or projects.")