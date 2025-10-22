
#!/usr/bin/env python3
"""
Dry-run (validation sans écriture en DB)
- Charge un CSV
- Typage intelligent (nombres, dates)
- Affiche NA/duplicates
"""
import argparse, os, sys, re
import pandas as pd

def smart_cast(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    for col in df2.columns:
        if re.search(r"(date|_at|_on)$", col, re.IGNORECASE):
            df2[col] = pd.to_datetime(df2[col], errors="coerce")
            continue
        df2[col] = pd.to_numeric(df2[col], errors="ignore")
    return df2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--id-field")
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print(f"CSV introuvable: {args.csv}", file=sys.stderr)
        sys.exit(2)

    df = pd.read_csv(args.csv)
    df = smart_cast(df)

    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Missing per column:", {c:int(df[c].isna().sum()) for c in df.columns})
    if args.id_field and args.id_field in df.columns:
        dups = df[args.id_field].astype(str).duplicated(keep=False).sum()
        print(f"Duplicates for '{args.id_field}':", int(dups))

if __name__ == "__main__":
    main()
