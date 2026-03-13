import os
import requests
import pandas as pd
from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

symbols = ["FFC","MCB","OGDC","MARI","SYS"]

data = []

for s in symbols:
    price = round(100 + hash(s) % 200,2)

    row = {
        "symbol": s,
        "price": price,
        "volume": 100000
    }

    data.append(row)

supabase.table("prices_daily").insert(data).execute()

print("Prices saved to Supabase")
