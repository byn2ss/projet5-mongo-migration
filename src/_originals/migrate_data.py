# --- Import des bibliothèques et définition des fonctions ---

import pandas as pd
import pymongo


# Charger le fichier CSV
file_path = 'healthcare_dataset.csv'
df = pd.read_csv(file_path)


# Automatiser les tests d'intégrité
def automate_tests(df, context=""):
    test_data_integrity(df, context)

# Exporter les données de MongoDB vers un fichier CSV
def export_to_csv_from_mongo(collection, output_file):
    cursor = collection.find()
    df_from_mongo = pd.DataFrame(list(cursor))
    df_from_mongo.to_csv(output_file, index=False)
    print(f"Les données ont été exportées vers {output_file}.")

# Importer les données d'un fichier CSV dans MongoDB
def import_from_csv_to_mongo(file_path, collection):
    df_to_import = pd.read_csv(file_path)
    for index, row in df_to_import.iterrows():
        document = row.to_dict()
        collection.insert_one(document)
    print(f"Les données ont été importées depuis {file_path} dans MongoDB.")

# Fonction pour tester l'intégrité des données
def test_data_integrity(df, context=""):
    """
    Fonction pour tester l'intégrité des données.
    context: description (avant ou après migration)
    """
    print(f"\n### Test d'intégrité {context} ###")
    print("\nColonnes disponibles :", list(df.columns))
    print("\nTypes des variables :\n", df.dtypes)
    print("\nNombre de doublons :", df.duplicated().sum())
    print("\nValeurs manquantes :\n", df.isnull().sum())
    print("\nNombre total de lignes :", len(df))
    print("Nombre total de colonnes :", len(df.columns))

# Tester l'intégrité des données avant le nettoyage
test_data_integrity(df, context="avant nettoyage")

# Afficher les doublons
print("Doublons:", df.duplicated().sum())  # Affiche le nombre de doublons

# Afficher les lignes doublons
print("Lignes doublons :")
print(df[df.duplicated()])  # Affiche les lignes doublons

# Afficher les informations de chaque colonne
print("Infos du DataFrame :")
print(df.info())  # Donne des informations sur chaque colonne

# Supprimer les doublons
df_cleaned = df.drop_duplicates()

# Vérifier que les doublons ont bien été supprimés
print("Doublons après nettoyage:", df_cleaned.duplicated().sum())

# Exporter les données nettoyées dans un fichier CSV si nécessaire
df_cleaned.to_csv('cleaned_healthcare_dataset.csv', index=False)

# Tester l'intégrité des données après le nettoyage
test_data_integrity(df_cleaned, context="après nettoyage")

# Charger le fichier CSV nettoyé
file_path = 'cleaned_healthcare_dataset.csv'
df = pd.read_csv(file_path)

# Connexion à MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['medical_data']  # Nom de la base de données
collection = db['patients']  # Nom de la collection

# Ajouter les données dans la collection MongoDB
for index, row in df.iterrows():
    document = {
        'Name': row['Name'],
        'Age': row['Age'],
        'Gender': row['Gender'],
        'Blood Type': row['Blood Type'],
        'Medical Condition': row['Medical Condition'],
        'Date of Admission': row['Date of Admission'],
        'Doctor': row['Doctor'],
        'Hospital': row['Hospital'],
        'Insurance Provider': row['Insurance Provider'],
        'Billing Amount': row['Billing Amount'],
        'Room Number': row['Room Number'],
        'Admission Type': row['Admission Type'],
        'Discharge Date': row['Discharge Date'],
        'Medication': row['Medication'],
        'Test Results': row['Test Results']
    }
    
    # Insérer le document dans la collection
    collection.insert_one(document)

print('Les données ont été migrées dans MongoDB.')

# Automatiser les tests d'intégrité après migration dans MongoDB
automate_tests(df_cleaned, "après migration dans MongoDB")

### Utilisation des CRUD (Create, Read, Update, Delete)

# Rechercher un patient par son nom
patient_name = "Bobby JacksOn"
patient_data = collection.find_one({'Name': patient_name})

# Vérifier si le patient a été trouvé
if patient_data:
    print("Données du patient trouvé :")
    print(patient_data)
else:
    print("Patient non trouvé.")


# 1. Ajouter un nouveau patient
new_patient = {
    'Name': 'John Doe',
    'Age': 30,
    'Gender': 'Male',
    'Blood Type': 'O+',
    'Medical Condition': 'Healthy',
    'Date of Admission': '2024-11-28',
    'Doctor': 'Dr. Smith',
    'Hospital': 'City Hospital',
    'Insurance Provider': 'HealthCorp',
    'Billing Amount': 500,
    'Room Number': 101,
    'Admission Type': 'Emergency',
    'Discharge Date': '2024-12-01',
    'Medication': 'None',
    'Test Results': 'Normal'
}
# Créer un index sur le champ 'Name' pour optimiser les recherches
collection.create_index([('Name', pymongo.ASCENDING)])  # Index ascendant sur le champ 'Name'

# Vérifier les indexes créés
indexes = collection.index_information()
print("Indexes existants dans la collection :", indexes)

# Ajouter le patient dans la collection
collection.insert_one(new_patient)
print("Nouveau patient ajouté.")

# 2. Modifier l'âge du patient
patient_name_to_update = 'John Doe'
new_age = 31  # Nouveau âge

# Utiliser update_one() pour mettre à jour l'âge
update_result = collection.update_one(
    {'Name': patient_name_to_update},  # Critère de recherche (nom du patient)
    {'$set': {'Age': new_age}}  # Mise à jour de l'âge
)

# Vérifier si l'âge a été modifié
if update_result.modified_count > 0:
    print(f"L'âge du patient {patient_name_to_update} a été mis à jour à {new_age}.")
else:
    print(f"Aucun changement trouvé pour le patient {patient_name_to_update}.")

# 3. Supprimer le patient
patient_name_to_delete = 'John Doe'

# Supprimer le patient
delete_result = collection.delete_one({'Name': patient_name_to_delete})

# Vérifier si le patient a été supprimé
if delete_result.deleted_count > 0:
    print(f"Le patient {patient_name_to_delete} a été supprimé.")
else:
    print(f"Aucun patient trouvé avec le nom {patient_name_to_delete}.")
# Rechercher un patient par son nom
patient_name = "John Doe"
patient_data = collection.find_one({'Name': patient_name})

# Vérifier si le patient a été trouvé
if patient_data:
    print("Données du patient trouvé :")
    print(patient_data)
else:
    print("Patient non trouvé.")


### Partie 2 : Conteneurisé avec Docker 
