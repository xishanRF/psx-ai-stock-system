import requests
import pandas as pd

symbols = ["FFC","MCB","OGDC","MARI","SYS"]

data = []

for s in symbols:
    price = round(100 + hash(s) % 200,2)
    data.append({
        "symbol":s,
        "price":price
    })

df = pd.DataFrame(data)

print("PSX Prices")
print(df)
