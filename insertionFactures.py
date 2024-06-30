import psycopg2
from datetime import datetime

# Connexion à la base de données
connection = psycopg2.connect(
    dbname="easyLawDb",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

try:
    # Données à insérer dans la table Users
    users_data = [
        (
            80,
            "scrypt:32768:8:1$DBxMgovT7H9MxiA6$c74db85587ed8603d324fc7a415072c14231f6013b6a132dcfc60c7b99fcae9e4777a0303a8874f02d7ae09b5e68287ccd43d1e0a8718d3f2e57e0dae46ac90e",
            "abbaci@esi.dz",
            datetime.strptime("2024-05-08 09:12:23.464882+0000", "%Y-%m-%d %H:%M:%S.%f%z"),
            "عباسي تسنيم",
            "admin",
            True,
            "1234567890"
        )
    ]

    # Insertion des données dans la table Users
    for user in users_data:
        cursor.execute("""
            INSERT INTO public."Users" (id, password, email, created_at, username, role, deleted, "phoneNumber")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, user)

    # Données à insérer dans la table Invoice
    invoices_data = [
        (
            1,
            "12-13",
            datetime.strptime("2024-05-28", "%Y-%m-%d"),
            4500.00,
            1,
            "gold_card",
            1,
            "kz_abbaci@esi.dz",
            "07939921328"
        ),
        (
            2,
            "14-17",
            datetime.strptime("2024-03-18", "%Y-%m-%d"),
            3200.00,
            1,
            "gold_card",
            2,
            "kz_abbaci@esi.dz",
            "07939921328"
        )
    ]

    # Insertion des données dans la table Invoice
    for invoice in invoices_data:
        cursor.execute("""
            INSERT INTO public."Invoice" (id, "numFacture", "dateFacture", "prixFacture", "idUser", "payment_Way", "idService", email, "phoneNumber")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, invoice)

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
