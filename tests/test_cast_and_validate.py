import pandas as pd

# On essaie d'importer depuis src.migrate (si jamais tu exposes smart_cast/validation_report),
# sinon on utilise les fallback _smart_cast/_validation_report ci-dessous.
HAS_FUNCS = False
try:
    from src.migrate import smart_cast, validation_report  # type: ignore
    HAS_FUNCS = True
except Exception:
    HAS_FUNCS = False

def _smart_cast(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    for c in df2.columns:
        lc = c.lower()
        # règle plus large : si le nom CONTIENT "date" ou se termine par _at/_on -> datetime
        if ("date" in lc) or lc.endswith(("_at","_on")):
            df2[c] = pd.to_datetime(df2[c], errors="coerce"); continue
        # numérique "safe"
        try:
            df2[c] = pd.to_numeric(df2[c])
        except Exception:
            pass
    return df2

def _validation_report(df: pd.DataFrame, id_field=None):
    rep = {
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "missing_counts": {c:int(df[c].isna().sum()) for c in df.columns},
    }
    if id_field and id_field in df.columns:
        dups = df[id_field].astype(str).duplicated(keep=False).sum()
        rep["duplicate_id_rows"] = int(dups)
        rep["id_unique_ok"] = bool(dups == 0)
    else:
        rep["duplicate_id_rows"] = None
        rep["id_unique_ok"] = None
    return rep

def test_typage_et_doublons():
    df = pd.DataFrame({
        "age":["34","xx"],
        "date_consultation":["2024-01-01","n/a"],
        "id":[1,1]
    })
    cast = (smart_cast(df) if HAS_FUNCS else _smart_cast(df))
    rep  = (validation_report(cast, "id") if HAS_FUNCS else _validation_report(cast, "id"))

    # vérifie bien la conversion en datetime64
    assert str(cast["date_consultation"].dtype).startswith("datetime64")
    # vérifie les doublons
    assert rep["duplicate_id_rows"] == 2
    assert rep["id_unique_ok"] is False
