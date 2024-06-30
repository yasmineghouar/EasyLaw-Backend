import pandas as pd
import psycopg2
from psycopg2 import Error

# Lecture des données à partir du fichier Excel
df = pd.read_excel('_majliss_table_data_cleaned.xlsx')

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

    for index, row in df.iterrows():
        # Insérer موضوع dans la table "sujet" s'il n'existe pas
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

        # Insérer غرفة dans la table "Chambre" s'il n'existe pas
        query = """
        INSERT INTO "Chambre" ("nom_chambre")
        VALUES (%s)
        ON CONFLICT DO NOTHING
        """
        data = (row['الغرفة'],)
        cursor.execute(query, data)

        # Insérer قسم dans la table "Classe" s'il n'existe pas
        query = """
        INSERT INTO "Classe" ("nom_classe")
        VALUES (%s)
        ON CONFLICT DO NOTHING
        """
        data = (row['القسم'],)
        cursor.execute(query, data)

        # Insérer التكييف dans la table "Takyif" s'il n'existe pas
        query = """
        INSERT INTO "Takyif" ("nom_takyif")
        VALUES (%s)
        ON CONFLICT DO NOTHING
        """
        data = (row['التكييف'],)
        cursor.execute(query, data)

        # Insérer les infos dans la table "QrarMajliss"
        query = """
        INSERT INTO "QrarMajliss" ("chambre", "classe", "takyif", "num_qarar")
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM "QrarMajliss" WHERE "num_qarar" = %s
        )
        """
        data = (row['الغرفة'], row['القسم'], row['التكييف'], row['رقم القرار'], row['رقم القرار'])
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
