#!/usr/bin/env python3
import argparse, os, sys, json, re
import pandas as pd
from pymongo import MongoClient, ASCENDING

def smart_cast(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes en types appropriés (Dates, Numérique)."""
    df2 = df.copy()
    for col in df2.columns:
        lc = col.lower()
        if ("date" in lc) or lc.endswith(("_at","_on")):https://github.com/byn2ss/projet5-mongo-migration
            df2[col] = pd.to_datetime(df2[col], errors="coerce")
            continue
        try:
            df2[col] = pd.to_numeric(df2[col])
        except Exception:
            pass
    return df2

def validation_report(df: pd.DataFrame, id_field=None):
    """Génère un rapport de qualité des données avant l'insertion."""
    rep = {
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "columns": {c: str(df[c].dtype) for c in df.columns},
        "missing_counts": {c: int(df[c].isna().sum()) for c in df.columns},
    }
    if id_field and id_field in df.columns:
        dups = df[id_field].astype(str).duplicated(keep=False).sum()
        rep["duplicate_id_rows"] = int(dups)
        rep["id_unique_ok"] = bool(dups == 0)
    else:
        rep["duplicate_id_rows"] = None
        rep["id_unique_ok"] = None
    return rep

def to_docs(df: pd.DataFrame):
    """Convertit le DataFrame en liste de dictionnaires pour MongoDB."""
    out = []
    for rec in df.to_dict(orient="records"):
        for k, v in list(rec.items()):
            if hasattr(v, "to_pydatetime"):
                rec[k] = v.to_pydatetime()
        out.append(rec)
    return out

def py_convert(obj):
    """Assure que tous les types sont compatibles JSON (nettoyage final)."""
    try:
        import numpy as np
        if isinstance(obj, (np.integer,)):  return int(obj)
        if isinstance(obj, (np.floating,)): return float(obj)
        if isinstance(obj, (np.bool_,)):    return bool(obj)
    except Exception:
        pass
    if isinstance(obj, dict):
        return {k: py_convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [py_convert(v) for v in obj]
    return obj

if __name__ == "__main__":
    # 1. Configuration des arguments de ligne de commande
    ap = argparse.ArgumentParser(description="Pipeline ETL : CSV vers MongoDB")
    ap.add_argument("--csv", required=True, help="Chemin du fichier source")
    ap.add_argument("--export-json", help="Nom du fichier pour l'export de contrôle")
    ap.add_argument("--mongo-uri", required=True, help="Lien de connexion MongoDB")
    ap.add_argument("--db", required=True, help="Nom de la base de données")
    ap.add_argument("--collection", required=True, help="Nom de la collection")
    ap.add_argument("--id-field", help="Champ utilisé comme clé unique (pivot)")
    args = ap.parse_args()

    # 2. Vérification de l'existence du fichier
    if not os.path.exists(args.csv):
        print(f"❌ Erreur : CSV introuvable à l'adresse {args.csv}", file=sys.stderr)
        sys.exit(2)

    # 3. Lecture et Transformation (ETL - T)
    print(f"📖 Lecture de {args.csv}...")
    df = pd.read_csv(args.csv)
    df = smart_cast(df)

    # 4. Génération du rapport de validation
    rep = validation_report(df, args.id_field)
    rep = py_convert(rep)
    with open("validation_report.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print("📊 Rapport de validation généré : validation_report.json")

    # 5. Connexion à MongoDB (ETL - L)
    client = MongoClient(args.mongo_uri)
    coll = client[args.db][args.collection]

    # Création d'un index si un champ ID est spécifié
    if args.id_field and args.id_field in df.columns:
        coll.create_index([(args.id_field, ASCENDING)], name=f"idx_{args.id_field}")

    # Préparation des documents
    docs = to_docs(df)
    
    # 6. Insertion ou Upsert
    if args.id_field and args.id_field in df.columns:
        from pymongo import UpdateOne
        ops = [UpdateOne({args.id_field: d.get(args.id_field)}, {"$set": d}, upsert=True) for d in docs]
        if ops:
            coll.bulk_write(ops, ordered=False)
        print(f"🔄 Upsert terminé : {len(docs)} documents traités via {args.id_field}.")
    else:
        if docs:
            coll.insert_many(docs, ordered=False)
        print(f"📥 Insertion terminée : {len(docs)} nouveaux documents créés.")

    # 7. Export optionnel (pour vérification)
    if args.export_json:
        out = []
        for doc in coll.find({}):
            doc.pop("_id", None)
            for k, v in list(doc.items()):
                if hasattr(v, "isoformat"):
                    doc[k] = v.isoformat()
            out.append(py_convert(doc))
        with open(args.export_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"📦 Export JSON créé : {args.export_json}")

    # 8. NETTOYAGE FINAL (Sécurité GitHub)
    # On ne supprime que si l'insertion s'est déroulée sans erreur
    try:
        if os.path.exists(args.csv):
            os.remove(args.csv)
            print(f"🗑️ Nettoyage de sécurité : Le fichier {args.csv} a été supprimé.")
            print("🚀 Processus terminé avec succès. Aucune donnée sensible ne reste dans le dossier data.")
    except Exception as e:
        print(f"⚠️ Alerte : Impossible de supprimer le fichier source : {e}")
