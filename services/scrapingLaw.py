# scraping_script.py
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import pandas as pd
import re
import psycopg2
from urllib.parse import urlparse
from ..app import db
from ..models.law import Law 
from sqlalchemy.exc import SQLAlchemyError
import sys
import csv
import os
import requests
import csv
from datetime import datetime

 
def process_data():
    df = pd.read_csv("table_data2.csv", header=None, encoding='utf-8')
    organized_data = [] 
    temp_lines = []

    for index, row in df.iterrows():
        if '[التفاصيل]' in str(row.values):
            if temp_lines:
                organized_data.append(temp_lines)
                temp_lines = []
        else:
            temp_lines.append(row.values[0])

    if temp_lines:
        organized_data.append(temp_lines)

    df_output = pd.DataFrame(organized_data)
    df_output.to_csv("organized_data.csv", index=False, header=False)

    df = pd.read_csv("organized_data.csv", header=None, encoding='utf-8')
    df = df.iloc[:, :4]
    column_names = ["القانون", "وزارة", "الجريدة", "الموضوع"]
    df.columns = column_names[:df.shape[1]]

    for index, row in df.iterrows():
        if isinstance(row['الجريدة'], str) and not row['الجريدة'].startswith('الجريدة'):
            df.at[index, 'الموضوع'] = row['الجريدة']
            df.at[index, 'الجريدة'] = row['وزارة']

    df.to_csv("modified_data.csv", index=False, encoding='utf-8')

    df = pd.read_csv("modified_data.csv", header=None, encoding='utf-8', skiprows=1)
    df.columns = ["القانون", "wizara", "الجريدة", "sujet"]
    df['type'] = df['القانون'].apply(lambda x: x.split(" رقم ")[0].strip() if pd.notnull(x) else None)
    df['num'] = df['القانون'].apply(lambda x: x.split(" رقم ")[1].split(" ممضي ")[0].strip() if pd.notnull(x) and " رقم " in x else None)
    df['date'] = df['القانون'].apply(lambda x: x.split(" ممضي في ")[1].strip() if pd.notnull(x) and " ممضي في " in x else None)
    df['num_jarida'] = df['الجريدة'].apply(lambda x: x.split("عدد")[1].split("مؤرخة")[0].strip() if pd.notnull(x) and "عدد" in x else None)
    df['date_jarida'] = df['الجريدة'].apply(lambda x: x.split(" في ")[1].split(" الصفحة ")[0].strip() if pd.notnull(x) and " في " in x else None)
    df['page_jarida'] = df['الجريدة'].apply(lambda x: x.split(" الصفحة ")[1].strip() if pd.notnull(x) and " الصفحة " in x else None)

    df = df.dropna(how='all')
    df.drop(columns=["القانون"], inplace=True)
    df.drop(columns=["الجريدة"], inplace=True)

    df.to_csv("structured_data.csv", index=False, encoding='utf-8')
    
    try:
        os.remove("table_data2.csv")
        print("Le fichier table_data2.csv a été supprimé avec succès.")
    except FileNotFoundError:
        print("Le fichier table_data2.csv n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la suppression de table_data2.csv : {e}")


# def add_domains():
#     DATABASE_URL = "postgresql://postgres:@localhost:5432/easyLawDb"
#     url = urlparse(DATABASE_URL)
#     conn = psycopg2.connect(
#         dbname=url.path[1:],
#         user=url.username,
#         password=url.password,
#         host=url.hostname,
#         port=url.port
#     )

#     def extraire_domaines_mots_cles():
#         domaines_mots_cles = {}
#         try:
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT d.nom AS domaine, m.nom AS mot_cle 
#                 FROM public."interestedDomain" d
#                 JOIN public."motsCles" m ON d.id = m."idInterestedDomain"
#             """)
#             rows = cur.fetchall()
#             for domaine, mot_cle in rows:
#                 if domaine not in domaines_mots_cles:
#                     domaines_mots_cles[domaine] = []
#                 domaines_mots_cles[domaine].append(mot_cle)
#         finally:
#             cur.close()
#         return domaines_mots_cles

#     def determiner_domaines(texte, domaines_mots_cles):
#         domaines_texte = []
#         for domaine, mots_cles in domaines_mots_cles.items():
#             for mot_cle in mots_cles:
#                 if re.search(r'\b' + re.escape(mot_cle) + r'\b', texte, flags=re.IGNORECASE):
#                     domaines_texte.append(domaine)
#                     break
#         return domaines_texte if domaines_texte else ["Non spécifié"]

#     domaines = extraire_domaines_mots_cles()
#     fichier_entree = "structured_data.csv"
#     fichier_sortie = "structured_data_avec_domaines.csv"

#     with open(fichier_entree, mode='r', newline='', encoding='utf-8') as f_entree, \
#          open(fichier_sortie, mode='w', newline='', encoding='utf-8') as f_sortie:

#         lecteur_csv = csv.DictReader(f_entree)
#         entetes = lecteur_csv.fieldnames + ['مجال']

#         writer = csv.DictWriter(f_sortie, fieldnames=entetes)
#         writer.writeheader()

#         for ligne in lecteur_csv:
#             sujet = ligne['sujet']
#             domaines_texte = determiner_domaines(sujet, domaines)
#             ligne['مجال'] = ", ".join(domaines_texte)
#             writer.writerow(ligne)

#     conn.close()

def add_domains():
    DATABASE_URL = "postgresql://postgres:@localhost:5432/easyLawDb"
    url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    def extraire_domaines_mots_cles():
        domaines_mots_cles = {}
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT d.nom AS domaine, m.nom AS mot_cle 
                FROM public."interestedDomain" d
                JOIN public."motsCles" m ON d.id = m."idInterestedDomain"
            """)
            rows = cur.fetchall()
            for domaine, mot_cle in rows:
                if domaine not in domaines_mots_cles:
                    domaines_mots_cles[domaine] = []
                domaines_mots_cles[domaine].append(mot_cle)
        finally:
            cur.close()
        return domaines_mots_cles

    def determiner_domaines(texte, domaines_mots_cles):
        domaines_texte = set()  # Use a set to avoid duplicate domains
        for domaine, mots_cles in domaines_mots_cles.items():
            for mot_cle in mots_cles:
                if re.search(r'\b' + re.escape(mot_cle) + r'\b', texte, flags=re.IGNORECASE):
                    domaines_texte.add(domaine)
        return list(domaines_texte) if domaines_texte else ["Non spécifié"]

    domaines = extraire_domaines_mots_cles()
    fichier_entree = "structured_data.csv"
    fichier_sortie = "structured_data_avec_domaines.csv"

    with open(fichier_entree, mode='r', newline='', encoding='utf-8') as f_entree, \
         open(fichier_sortie, mode='w', newline='', encoding='utf-8') as f_sortie:

        lecteur_csv = csv.DictReader(f_entree)
        entetes = lecteur_csv.fieldnames + ['مجال']

        writer = csv.DictWriter(f_sortie, fieldnames=entetes)
        writer.writeheader()

        for ligne in lecteur_csv:
            sujet = ligne['sujet']
            domaines_texte = determiner_domaines(sujet, domaines)
            ligne['مجال'] = ", ".join(domaines_texte)
            writer.writerow(ligne)

    conn.close()



def insert_data():
    DATABASE_URL = "postgresql://postgres:@localhost:5432/easyLawDb"
    url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password, 
        host=url.hostname,
        port=url.port
    )

    fichier_csv = "structured_data_avec_domaines.csv"

    with open(fichier_csv, mode='r', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.DictReader(csvfile)
        for ligne in lecteur_csv:
            wizara = str(ligne['wizara'])
            sujet = str(ligne['sujet'])
            type = str(ligne['type'])
            num = str(ligne['num'])
            date = str(ligne['date'])
            num_jarida = str(ligne['num_jarida'])
            date_jarida = str(ligne['date_jarida'])
            page_jarida = str(ligne['page_jarida'])
            مجال = str(ligne['مجال'])

            updated_at = datetime.now()
            
            sql = """
            INSERT INTO public.law (wizara, sujet, type, num, date, num_jarida, date_jarida, page_jarida, مجال , updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cur = conn.cursor()
            cur.execute(sql, (wizara, sujet, type, num, date, num_jarida, date_jarida, page_jarida, مجال , updated_at))
            conn.commit()
            cur.close()

    conn.close()
    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        csvfile.truncate()

def is_file_empty(filename):
    return os.path.exists(filename) and os.path.getsize(filename) == 0

