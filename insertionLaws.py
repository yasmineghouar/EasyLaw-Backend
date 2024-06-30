import re
import csv
import psycopg2
import os
from urllib.parse import urlparse

# Extraction des informations de connexion de l'URL
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

# Lecture du fichier CSV et insertion des données dans la table law
with open(fichier_sortie, mode='r', newline='', encoding='utf-8') as csvfile:
    lecteur_csv = csv.DictReader(csvfile)
    for ligne in lecteur_csv:
        # Convertir les variables en chaînes si nécessaire
        wizara = str(ligne['wizara'])
        sujet = str(ligne['sujet'])
        type = str(ligne['type'])
        num = str(ligne['num'])
        date = str(ligne['date'])
        num_jarida = str(ligne['num_jarida'])
        date_jarida = str(ligne['date_jarida'])
        page_jarida = str(ligne['page_jarida'])
        مجال = str(ligne['مجال'])

        # Construction de la requête SQL d'insertion
        sql = """
        INSERT INTO public.law (wizara, sujet, type, num, date, num_jarida, date_jarida, page_jarida, مجال)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Exécution de la requête SQL
        cur = conn.cursor()
        cur.execute(sql, (wizara, sujet, type, num, date, num_jarida, date_jarida, page_jarida, مجال))
        conn.commit()
        cur.close()

print("Les données ont été insérées avec succès dans la table law.")

# Fermer la connexion à la base de données
conn.close()
