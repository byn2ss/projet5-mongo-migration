#!/usr/bin/env python3
import argparse, os, sys, json, re
import pandas as pd
from pymongo import MongoClient, ASCENDING

def smart_cast(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    for col in df2.columns:
        lc = col.lower()
        if ("date" in lc) or lc.endswith(("_at","_on")):
            df2[col] = pd.to_datetime(df2[col], errors="coerce"); continue
        # Conversion numérique "safe" (sans errors="ignore")
        try:
            df2[col] = pd.to_numeric(df2[col])
        except Exception:
            pass
    return df2

def validation_report(df: pd.DataFrame, id_field=None):
    rep = {
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "columns": {c: str(df[c].dtype) for c in df.columns},
        "missing_counts": {c:int(df[c].isna().sum()) for c in df.columns},
    }
    if id_field and id_field in df.columns:
        dups = df[id_field].astype(str).duplicated(keep=False).sum()
        rep["duplicate_id_rows"] = int(dups)
        rep["id_unique_ok"] = bool(dups == 0)  # <- bool Python natif
    else:
        rep["duplicate_id_rows"] = None
        rep["id_unique_ok"] = None
    return rep

def to_docs(df: pd.DataFrame):
    out = []
    for rec in df.to_dict(orient="records"):
        # Convertir les Timestamp -> datetime natif
        for k,v in list(rec.items()):
            if hasattr(v, "to_pydatetime"):
                rec[k] = v.to_pydatetime()
        out.append(rec)
    return out

def py_convert(obj):
    """Convertit récursivement les types numpy/pandas en types Python natifs."""
    try:
        import numpy as np
        if isinstance(obj, (np.integer,)):  return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, (np.bool_,)):    return bool(obj)
    except Exception:
        pass
    if isinstance(obj, dict):
        return {k: py_convert(v) for k,v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [py_convert(v) for v in obj]
    return obj

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="CSV -> MongoDB (CLI prêt)")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--export-json")
    ap.add_argument("--mongo-uri", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--id-field")
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print(f"CSV introuvable: {args.csv}", file=sys.stderr); sys.exit(2)

    df = pd.read_csv(args.csv)
    df = smart_cast(df)

    rep = validation_report(df, args.id_field)
    rep = py_convert(rep)  # <- conversion avant JSON
    with open("validation_report.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print("Validation report -> validation_report.json")

    client = MongoClient(args.mongo_uri)
    coll = client[args.db][args.collection]

    if args.id_field and args.id_field in df.columns:
        coll.create_index([(args.id_field, ASCENDING)], name=f"idx_{args.id_field}", unique=False)

    docs = to_docs(df)
    if args.id_field and args.id_field in df.columns:
        from pymongo import UpdateOne
        ops = [UpdateOne({args.id_field: d.get(args.id_field)}, {"$set": d}, upsert=True) for d in docs]
        if ops: coll.bulk_write(ops, ordered=False)
        print(f"Upsert by {args.id_field}: {len(docs)} rows")
    else:
        if docs: coll.insert_many(docs, ordered=False)
        print(f"Inserted: {len(docs)} rows")

    if args.export_json:
        out = []
        for doc in coll.find({}):
            doc.pop("_id", None)
            for k, v in list(doc.items()):
                if hasattr(v, "isoformat"):
                    doc[k] = v.isoformat()
            out.append(py_convert(doc))  # <- conversion aussi à l'export
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Exported -> {args.export_json}")
