import pandas as pd

files = ["annex1.csv", "annex2.csv", "annex3.csv", "annex4.csv"]

for f in files:
    print("\n======", f, "======")
    
    try:
        df = pd.read_csv(f)
    except UnicodeDecodeError:
        df = pd.read_csv(f, encoding="latin-1")
    
    print("\n--- HEAD ---")
    print(df.head())
    
    print("\n--- INFO ---")
    print(df.info())
