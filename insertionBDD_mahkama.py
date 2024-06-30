import pandas as pd
import psycopg2
from psycopg2 import Error
from datetime import datetime

# Lecture des données à partir du fichier Excel
df = pd.read_excel('mahkama_data_table.csv')

# Convertir le type de données de la colonne "تاريخ القرار" en chaîne de caractères (string)
df['تاريخ القرار'] = df['تاريخ القرار'].astype(str)
# Convertir le format de date dans le DataFrame
df['تاريخ القرار'] = df['تاريخ القرار'].str.replace('/', '-')

# Connexion à la base de données PostgreSQL
try:
    connection = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="easyLawDb"
    )

    cursor = connection.cursor()

    # Insertion des données dans les tables appropriées
    for index, row in df.iterrows():

        # Insérer "الموضوع" dans la table "sujet" s'il n'existe pas déjà
        query = """
        INSERT INTO "sujet" ("Nomsujet")
        SELECT %s
        WHERE NOT EXISTS (
            SELECT 1 FROM "sujet" WHERE "Nomsujet" = %s
        )
        """
        data = (row['الموضوع'], row['الموضوع'])
        cursor.execute(query, data)

        # Insérer les infos dans la table "Qrar"
        query = """
        INSERT INTO "Qrar" ("raqmQarar", "dataQarar", "sujetQarar", "principe")
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        """
        data = (row['رقم القرار'], row['تاريخ القرار'], row['الموضوع'], row['المبدأ'])
        cursor.execute(query, data)

        # Insérer les infos dans la table "QrarMahkama"
        query = """
        INSERT INTO "QrarMahkama" ("refLegale", "motsClés", "parties", "repMahkama", "OperatDecision", "raqmQararOrigin")
        SELECT %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM "QrarMahkama" WHERE "raqmQararOrigin" = %s
        )
        """
        data = (row['المرجع القانوني'], row['الكلمات الأساسية'], row['الأطراف'], row['رد المحكمة العليا'], row['منطوق القرار'], row['رقم القرار'], row['رقم القرار'])
        cursor.execute(query, data)

    connection.commit()
    print("Les données ont été insérées avec succès dans la base de données")

except (Exception, Error) as error:
    print("Erreur lors de la connexion à PostgreSQL ou lors de l'insertion des données :", error)

finally:
    # Fermer la connexion à la base de données
    if connection:
        cursor.close()
        connection.close()
        print("Connexion à PostgreSQL fermée")
