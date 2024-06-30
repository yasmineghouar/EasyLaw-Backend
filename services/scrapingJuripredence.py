import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import pandas as pd
import psycopg2
from psycopg2 import Error
from urllib.parse import urlparse
from sqlalchemy.orm import joinedload
from ..models.ijtihad import Qrar 
from ..models.interestedDomain import MotsCles 
from ..app import db




def cleaningMajliss():
    try:
        df = pd.read_csv("majliss.csv", header=None, encoding='utf-8', skiprows=1)
    except FileNotFoundError:
        return "Fichier 'majliss.csv' non trouvé."
    if df.empty:
        return "Le fichier 'majliss.csv' est vide."
    df = df.iloc[:, ::-1]  # Sélectionner toutes les lignes et inverser l'ordre des colonnes
    df = df.drop(df.columns[0], axis=1)
    df.columns = ["المبدأ", "الموضوع", "التكييف", "تاريخ القرار", "القسم", "الغرفة", "رقم القرار"]
    df.to_csv("_majliss_table_data_cleaned.csv", index=False, encoding='utf-8')

    return "Le nettoyage des données du fichier 'majliss.csv' a été effectué avec succès."


def insertJuriMajliss():
    # Lecture des données à partir du fichier Excel
    df = pd.read_csv('_majliss_table_data_cleaned.csv')

    # Connexion à la base de données PostgreSQL
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="",
            host="localhost",
            port="5432",
            database="easyLawDb"
        )

        cursor = connection.cursor()

        for index, row in df.iterrows():
            # Insérer موضوع dans la table "الموضوع" si il n'existe pas
            query = """
            INSERT INTO "sujet" ("Nomsujet") 
            SELECT %s 
            WHERE NOT EXISTS (SELECT 1 FROM "sujet" WHERE "Nomsujet" = %s)
            """
            data = (row['الموضوع'], row['الموضوع'])
            cursor.execute(query, data)

            updated_at = datetime.now()

            # Insérer les infos dans la table "قرار"
            query = """
            INSERT INTO "Qrar" ("raqmQarar", "dataQarar", "sujetQarar", "principe" , "updated_at") 
            VALUES (%s, %s, %s, %s,%s) 
            ON CONFLICT DO NOTHING
            """
            data = (row['رقم القرار'], row['تاريخ القرار'], row['الموضوع'], row['المبدأ'], updated_at)
            cursor.execute(query, data)

            # Insérer غرفة dans la table "الغرفة" si il n'existe pas
            query = """
            INSERT INTO "Chambre" ("nom_chambre") 
            VALUES (%s) 
            ON CONFLICT DO NOTHING
            """
            data = (row['الغرفة'],)
            cursor.execute(query, data)

            # Insérer قسم dans la table "القسم" si il n'existe pas
            query = """
            INSERT INTO "Classe" ("nom_classe") 
            VALUES (%s) 
            ON CONFLICT DO NOTHING
            """
            data = (row['القسم'],)
            cursor.execute(query, data)

            # Insérer التكييف dans la table "التكييف" si il n'existe pas
            query = """
            INSERT INTO "Takyif" ("nom_takyif") 
            VALUES (%s) 
            ON CONFLICT DO NOTHING
            """
            data = (row['التكييف'],)
            cursor.execute(query, data)

            # Insérer dans la table "QrarMajliss"
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
 

# def update_qrar_domain():
#     qrar_entries = Qrar.query.all()
#     mots_cles_entries = MotsCles.query.options(joinedload(MotsCles.interested_domain)).all()

#     for qrar in qrar_entries:
#         found_domain = None
#         for mot_cle in mots_cles_entries:
#             if mot_cle.nom in qrar.principe:
#                 found_domain = mot_cle.interested_domain.nom
#                 break

#         if found_domain:
#             qrar.مجال = found_domain

#     db.session.commit()


def update_qrar_domain():
    qrar_entries = Qrar.query.all()
    mots_cles_entries = MotsCles.query.options(joinedload(MotsCles.interested_domain)).all()

    for qrar in qrar_entries:
        found_domains = []
        for mot_cle in mots_cles_entries:
            if mot_cle.nom in qrar.principe:
                found_domains.append(mot_cle.interested_domain.nom)

        if found_domains:
            qrar.مجال = ', '.join(found_domains)  # Joindre les domaines par une virgule et un espace ou tout autre séparateur de votre choix

    db.session.commit()

