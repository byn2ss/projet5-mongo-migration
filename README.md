Parfait 👍 voici ton **README complet**, 100 % corrigé, sans emoji, avec la structure du projet correctement formatée.
Tu peux **copier-coller ce bloc entier** dans ton fichier `README.md` sur VS Code.

---

```markdown
# Projet 5 – Migration des données médicales vers MongoDB (Docker + CI + Cloud)

## Contexte

Ce projet a été réalisé dans le cadre de ma mission en tant que Data Engineer chez DataSoluTech.  
L’objectif est de migrer un dataset de données médicales de patients (au format CSV) vers une base MongoDB, afin d’assurer une meilleure scalabilité, performance et sécurité.

Ce projet intègre la conteneurisation Docker, la validation des données, les tests unitaires et l’intégration continue (CI) via GitHub Actions.

---

## Objectifs du projet

- Migrer les données CSV vers MongoDB  
- Conteneuriser MongoDB et le script de migration avec Docker  
- Vérifier l’intégrité et le typage des données avant et après migration  
- Automatiser les tests unitaires avec Pytest  
- Mettre en place une pipeline CI/CD avec GitHub Actions  
- Documenter et versionner le projet pour assurer sa maintenabilité  

---

## Stack technique

| Outil / Technologie | Rôle |
|----------------------|------|
| Python 3.11 | Développement du script de migration |
| Pandas | Lecture et transformation du CSV |
| PyMongo | Connexion et insertion dans MongoDB |
| MongoDB 7 | Base NoSQL pour stocker les données médicales |
| Docker / Docker Compose | Conteneurisation de MongoDB |
| Pytest | Tests unitaires |
| GitHub Actions | Intégration continue |
| VS Code | Environnement de développement |

---

## Structure du projet

```

projet5-mongo-migration/
├── src/                     # Scripts Python principaux
│   ├── migrate.py           # Fonctions de migration
│   └── migrate_cli.py       # Interface CLI pour exécuter la migration
├── scripts/
│   └── migrate_dry_run.py   # Validation des données (sans insertion)
├── tests/
│   └── test_cast_and_validate.py # Tests unitaires Pytest
├── data/
│   └── patients_sample.csv  # Dataset d'exemple
├── docker-compose.yml       # Déploiement MongoDB
├── requirements.txt         # Dépendances Python
├── README.md                # Documentation du projet
└── .github/workflows/ci.yml # Pipeline CI

````

---

## Installation et exécution

### 1. Cloner le dépôt
```bash
git clone git@github.com:byn2ss/projet5-mongo-migration.git
cd projet5-mongo-migration
````

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Démarrer MongoDB avec Docker

```bash
docker compose up -d
```

### 4. Vérifier le conteneur MongoDB

```bash
docker ps
```

### 5. Vérification à blanc

```bash
python scripts/migrate_dry_run.py --csv data/patients_sample.csv --id-field id
```

### 6. Exécuter la migration réelle

```bash
python src/migrate_cli.py \
  --csv data/patients_sample.csv \
  --export-json out.json \
  --mongo-uri "mongodb://admin:admin123@localhost:27017/?authSource=admin" \
  --db clinique \
  --collection patients \
  --id-field id
```

---

## Tests unitaires

Exécuter les tests :

```bash
pytest
```

Vérifie :

* la conversion automatique des champs “date” en datetime
* la détection des doublons sur l’ID
* la bonne structure du DataFrame après casting

---

## Docker

Le conteneur MongoDB est défini dans `docker-compose.yml` :

```yaml
services:
  mongo-medical:
    image: mongo:7
    container_name: mongo-medical
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin123
```

---

## Intégration continue (CI)

Le workflow GitHub Actions (`.github/workflows/ci.yml`) :

* s’exécute sur les branches main, develop et feature/*
* installe les dépendances
* lance les tests Pytest automatiquement

![Tests](https://github.com/byn2ss/projet5-mongo-migration/actions/workflows/ci.yml/badge.svg)

---

## Sécurité et utilisateurs MongoDB

Des utilisateurs sont créés lors de l’initialisation :

* admin : droits complets sur toutes les bases
* nurse : lecture seule sur la base clinique

Connexion avec authentification :

```bash
mongodb://admin:admin123@localhost:27017/?authSource=admin
```

---

## Résultats du projet

* Migration CSV → MongoDB réussie
* Validation des données automatisée
* Pipeline CI opérationnelle (tests automatisés)
* Documentation complète et claire
* Projet prêt pour le déploiement cloud (AWS, DocumentDB)

---

## Hébergement Cloud (optionnel – extension projet)

Le projet a été conçu pour pouvoir être facilement déployé sur le Cloud, notamment via AWS.
Voici les principales options d’intégration :

### 1. AWS DocumentDB (compatible MongoDB)

* Héberge la base de données MongoDB dans un environnement managé et sécurisé.
* Connexion identique à MongoDB local :

  ```bash
  mongodb+srv://admin:<password>@cluster0.<id>.amazonaws.com/clinique
  ```
* Gère automatiquement les sauvegardes, la haute disponibilité et le chiffrement.

### 2. AWS S3

* Stockage des fichiers CSV et exports JSON (patients_sample.csv, out.json, validation_report.json).
* Intégration directe via boto3 :

  ```python
  import boto3
  s3 = boto3.client('s3')
  s3.upload_file('out.json', 'mon-bucket-s3', 'exports/out.json')
  ```

### 3. AWS ECS ou Docker Hub

* Hébergement du conteneur MongoDB et du script de migration avec Docker.
* Build et push :

  ```bash
  docker build -t projet5-mongo .
  docker tag projet5-mongo byn2ss/projet5-mongo:latest
  docker push byn2ss/projet5-mongo:latest
  ```
* Puis déploiement sur ECS ou sur une VM EC2 via `docker compose up -d`.

### 4. Monitoring et sécurité

* Utilisation de CloudWatch pour suivre les logs et performances MongoDB.
* Authentification IAM et rotation automatique des clés d’accès.

Cette architecture permet une migration complète, scalable et sécurisée des données médicales vers le cloud AWS.



