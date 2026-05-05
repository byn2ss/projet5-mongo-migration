# Projet 5 – Migration des données médicales vers MongoDB (Docker + CI + Cloud)

## 🎯 Contexte

Ce projet a été réalisé dans le cadre de ma mission en tant que Data Engineer chez DataSoluTech.  
L’objectif client : migrer un dataset médical CSV dans une base MongoDB afin de garantir **scalabilité**, **performance**, **sécurité** et **maintenabilité**.

Ce projet inclut : 🚀  
✔ Conteneurisation (MongoDB + script de migration)  
✔ Validation & typage des données  
✔ Tests unitaires & CI/CD GitHub Actions  
✔ Documentation complète & prête pour audit technique  
✔ Architecture Cloud AWS (DocumentDB et S3)

---
Schemas du processus de migration : 

<img width="892" height="431" alt="schema_migration" src="https://github.com/user-attachments/assets/f323483e-84c6-4b11-a6b5-a744215867fa" />
e projet repose sur un flux de données automatisé et conteneurisé, structuré autour de trois piliers :

1. Le Flux ETL (Horizontal)

EXTRACT : Récupération des données brutes depuis un fichier CSV via un volume Docker.

TRANSFORM : Traitement par scripts Python (nettoyage, typage des données et génération du hash patient_id).

LOAD : Chargement final des données transformées dans MongoDB (conversion CSV vers BSON).

2. Infrastructure & Orchestration

L'intégralité du pipeline est isolée sous Docker pour garantir :

Conteneurisation : Isolation des services Python et MongoDB.

Orchestration : Communication sécurisée et automatisée entre les services via un réseau dédié.

3. Points Forts de l'Architecture

Modularité : Séparation stricte entre le traitement et le stockage, facilitant la maintenance.

Automatisation : Pipeline complet exécutable via une commande unique (docker-compose up).

Reproductibilité : Environnement identique quel que soit le système hôte.

## 📊 Schéma de la base de données

Voici la structure de notre collection MongoDB `patients_records` :

![Schéma de la base de données](docs/schema_bdd.jpg) 
<img width="761" height="321" alt="schemascollectionpatient" src="https://github.com/user-attachments/assets/ad3d98b7-3486-4cbc-9737-fb3e6d2dc943" />


---

## 🧰 Stack technique

| Outil / Technologie | Rôle |
|----------------------|------|
| Python 3.11 | Développement du script de migration |
| Pandas | Lecture & transformation du CSV |
| PyMongo | Connexion & insertion MongoDB |
| MongoDB 7 | Base NoSQL scalable |
| Docker & Docker Compose | Conteneurisation |
| Pytest | Tests unitaires |
| GitHub Actions | Intégration continue |
| VS Code | IDE |

---

## 📁 Structure du projet

```plaintext
projet5-mongo-migration/
├── src/
│   ├── migrate.py
│   └── migrate_cli.py
├── scripts/
│   └── migrate_dry_run.py
├── tests/
│   └── test_cast_and_validate.py
├── data/
│   └── patients_sample.csv
├── docs/
│   └── schema_bdd.jpg
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

Installation & Exécution (100% Docker)
1️⃣ Cloner le dépôt
git clone git@github.com:byn2ss/projet5-mongo-migration.git
cd projet5-mongo-migration

2️⃣ Créer un fichier .env à la racine du projet
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=xxxxxx
MONGO_DB=clinique
MONGO_COLLECTION=patients

(Le .env est ignoré par Git → aucune fuite de secrets sur GitHub)

3️⃣ Lancer MongoDB + Migration automatique via Docker
docker compose up --build
Cela va automatiquement :

Démarrer MongoDB

Valider le fichier CSV

Insérer les données dans clinique.patients
capture d'écran dans le dossier docs

4️⃣ Vérifier le résultat

capture d'écran dans le dossier docs

📍 Base attendue : clinique
📍 Collection attendue : patients

🧪 Tests unitaires
pytest


Les tests garantissent :
✔ Typage correct (dates converties en datetime)
✔ Absence de doublons sur id
✔ Structure correcte du DataFrame

➡️ Automatisés dans GitHub Actions

🐳 Docker – Infrastructure du projet

Services Docker :

Service	Description
mongodb	Base de données NoSQL
migration	Service Python qui exécute la migration

Fonctionnalités Docker :
✔ 🔄 Volume persistant pour MongoDB
✔ 🌐 Réseau Docker privé (mongo_network)
✔ 📦 Migration lancée automatiquement

🔐 Authentification & Sécurité

Deux rôles MongoDB configurés :

Utilisateur	Rôle	Accès
admin	Administrateur	Écriture & administration
nurse	Lecture seule	Lecture sur clinique

🔸 Les identifiants exacts sont fournis via .env
🔸 Aucun mot de passe visible dans le code ou sur GitHub

☁️ Intégration Cloud AWS — Documentation fournie
Service AWS	Utilité
Amazon DocumentDB	Hébergement managé compatible MongoDB
Amazon ECS	Hébergement des conteneurs Docker
Amazon S3	Stockage CSV & exports JSON
Amazon CloudWatch	Logs & Monitoring
IAM	Contrôle d’accès & sécurité

➡️ Le projet est prêt pour un déploiement cloud
