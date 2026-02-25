import certifi
import requests
import os
from dotenv import load_dotenv

load_dotenv()

import pandas as pd

def convert_to_dataframe(response):
    items = response["data"]["boards"][0]["items_page"]["items"]

    data = []

    for item in items:
        row = {"name": item["name"]}

        for col in item["column_values"]:
            row[col["id"]] = col["text"]

        data.append(row)

    df = pd.DataFrame(data)
    return df

API_KEY = os.getenv("MONDAY_API_KEY")
print("API KEY VALUE:", repr(API_KEY))
URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def fetch_board_data(board_id):
    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            id
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """
   
    response = requests.post(
    URL,
    json={'query': query},
    headers=headers,
    verify=False
)
    return response.json()