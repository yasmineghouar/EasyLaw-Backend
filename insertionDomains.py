import psycopg2
from datetime import datetime

# Connexion à la base de données pour les deux sets d'insertions
connection = psycopg2.connect(
    dbname="easyLawDb",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

try:
    # Insérer les données pour les domaines et les mots-clés
    domains = {
        "السياسة": ["الحكومة", "الدولة", "رئيس", "الدستور", "الديموقراطية", "السياسات العامة", "السياسة الخارجية"],
        "الصحة": ["مستشفى", "الاطباء", "المستشفيات", "طبيب", "دواء", "الصيدلانية", "الصحة", "المرض", "العلاج"],
        "الجرائم": ["العقوبات", "تبييض الاموال", "الطعن"],
        "المالية": ["المالية", "ميزانية", "الضرائب", "الدفع", "اسعار", "الاستثمار", "النقود", "البورصة"]
    }

    for domain in domains.keys():
        cursor.execute("""
            INSERT INTO public."interestedDomain" (nom)
            VALUES (%s)
            RETURNING id
        """, (domain,))
        domain_id = cursor.fetchone()[0]

        for keyword in domains[domain]:
            cursor.execute("""
                INSERT INTO public."motsCles" (nom, "idInterestedDomain", created_at)
                VALUES (%s, %s, %s)
            """, (keyword, domain_id, datetime.now()))

    # Insérer les données pour scrapingInfo
    donnees_a_inserer = [
        (2, "juripredence", True, datetime.strptime("2015-06-12", "%Y-%m-%d")),
        (1, "laws", True, datetime.strptime("2024-04-21", "%Y-%m-%d"))
    ]

    for donnee in donnees_a_inserer:
        cursor.execute("""
            INSERT INTO public."scrapingInfo" (id, service, "autoScraping", "lastDate")
            VALUES (%s, %s, %s, %s)
        """, donnee)

    # Commit des transactions
    connection.commit()
    print("Données insérées avec succès.")

except psycopg2.Error as e:
    connection.rollback()  # Annuler toutes les opérations en cas d'erreur
    print(f"Erreur lors de l'insertion des données : {e}")

finally:
    # Fermeture de la connexion
    if cursor:
        cursor.close()
    if connection:
        connection.close()
