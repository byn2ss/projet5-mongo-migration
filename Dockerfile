FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code dans le conteneur
COPY . .

# Commande par défaut (sera écrasée par docker-compose pour le service migration)
CMD ["python", "src/migrate_cli.py", "--help"]
