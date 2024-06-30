import requests
import os
from bs4 import BeautifulSoup

def download_pdf(url, folder):
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Extraire le nom du fichier PDF à partir de l'URL
    filename = os.path.join(folder, url.split("/")[-1])

    # Télécharger le fichier PDF
    response = requests.get(url, verify=False)
    
    # Vérifier si la balise h1 existe dans le contenu de la page
    soup = BeautifulSoup(response.content, 'lxml')
    h1_tag = soup.find("h1")
    if h1_tag is not None:
        h1_content = h1_tag.text.strip()
        if h1_content == "Erreur de serveur":
            print("Impossible de télécharger le PDF car le serveur a renvoyé une erreur.")
            return False
    else:
        print("Balise <h1> non trouvée dans le contenu de la page.")

    # Écrire le contenu dans le fichier PDF
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Le fichier PDF a été téléchargé avec succès sous {filename}")
    return True

# Dossier de destination
folder = "uploads"

# Boucle sur les annees de 1965 à 2014
for year in range(2024,2025 ):    # Boucle de 1 à 120
    for num in range(1, 121):
        # Format de l'URL avec l'année et le numéro pour la première URL
        url = f"https://www.joradp.dz/FTP/jo-arabe/{year}/A{year}{num:03}.pdf"
        
        # Essayer de télécharger le PDF depuis la première URL
        if not download_pdf(url, folder):
            # Si erreur de serveur, essayer la deuxième URL
            url = f"https://www.joradp.dz/FTP/JO-ARABE/{year}/A{year}{num:03}.pdf"
            if not download_pdf(url, folder):
                # Si erreur de serveur sur les deux URLs, passer à l'itération suivante
                break  # Passer à l'itération suivante si erreur de serveur
