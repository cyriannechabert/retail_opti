import json
import pandas as pd

path = r"C:/Users/cycyc/retail_opti\DelightingCustomersBD.json"

with open(path, "r", encoding="utf-8") as f:
    raw = f.read()

print(raw[:500])  # print first 500 chars
