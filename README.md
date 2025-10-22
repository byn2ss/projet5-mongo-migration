# PROJET 5 — Migration CSV -> MongoDB (Prêt GitHub)

Ce dépôt est **prêt à publier** sur GitHub avec : séparation `src/scripts/tests/data`, CI, Docker et Makefile.

## 🚀 Démarrage rapide
```bash
make up
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Dry-run (validation sans écriture)
python scripts/migrate_dry_run.py --csv data/patients_sample.csv --id-field id

# Migration (écrit en DB + export JSON)
python src/migrate.py --csv data/patients_sample.csv --export-json out.json

# Tests
pytest -q
```

## 📁 Structure
```
src/                # script de production (écrit en DB)
  migrate.py        # (votre script principal a été importé ici)
  _originals/       # copies des .py originaux pour référence
scripts/            # outils de validation/dry-run
tests/              # tests pytest (typage + doublons)
data/               # CSV/JSON d'entrée
.github/workflows/  # CI GitHub Actions
docker-compose.yml  # Mongo local + volume
Makefile            # raccourcis (up/test/dry-run/migrate)
```

## 🔐 MongoDB (exemple de rôles)
Dans `mongosh` :
```js
use clinique
db.createUser({user:"doctor",pwd:"<mdp>",roles:[{role:"readWrite",db:"clinique"}]})
db.createUser({user:"nurse", pwd:"<mdp>",roles:[{role:"read",     db:"clinique"}]})
```

## 🌿 Branches Git
- `main` (stable, protégé)
- `develop` (intégration)
- `feature/<nom>`

## 💡 À adapter
- Si votre `src/migrate.py` n’expose pas `smart_cast`/`validation_report`, les tests utilisent une version fallback.
- Ajoutez des tests CLI/CRUD supplémentaires si besoin.
```

## Intégration continue
![Tests](https://github.com/byn2ss/projet5-mongo-migration/actions/workflows/ci.yml/badge.svg)
