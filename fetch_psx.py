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

WATCHLIST = ["FFC", "MCB", "OGDC", "MARI", "SYS"]

def main():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    payload = response.json()

    if payload.get("status") != "ok":
        raise Exception(f"API returned non-ok status: {payload}")

    rows = []

    for item in payload.get("data", []):
        market_type = item.get("m")
        symbol = item.get("s")
        price = item.get("c")

        if market_type != "REG":
            continue

        if symbol not in WATCHLIST:
            continue

        rows.append({
            "symbol": symbol,
            "price": price,
            "volume": None
        })

    if not rows:
        raise Exception("No matching watchlist symbols found in API response")

    supabase.table("prices_daily").insert(rows).execute()

    print("Inserted rows into prices_daily:")
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
