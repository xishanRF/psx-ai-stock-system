import os
import requests
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
CAPITALSTAKE_API_KEY = os.environ["CAPITALSTAKE_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

URL = "https://csapis.com/3.0/market/tickers"
HEADERS = {
    "Authorization": f"Bearer {CAPITALSTAKE_API_KEY}",
    "Accept": "application/json"
}

def main():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    payload = response.json()

    if payload.get("status") != "ok":
        raise Exception(f"API returned non-ok status: {payload}")

    rows = []

    for item in payload.get("data", []):
        if item.get("m") != "REG":
            continue

        rows.append({
            "symbol": item.get("s"),
            "price": item.get("c"),
            "volume": None
        })

    if not rows:
        raise Exception("No REG tickers returned")

    supabase.table("prices_daily").insert(rows).execute()

    print(f"Inserted {len(rows)} rows into prices_daily")

if __name__ == "__main__":
    main()
