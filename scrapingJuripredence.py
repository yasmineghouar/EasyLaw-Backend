import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import sys

# Configurer la journalisation
logging.basicConfig(filename='scrapingJuripredence.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Début du scraping...")
# Vérifier si les deux dates ont été fournies en arguments de ligne de commande
if len(sys.argv) != 3:
    logging.error("Veuillez fournir deux dates au format 'jour/mois/année' en arguments de ligne de commande.")
    sys.exit(1)

date_debut, date_fin = sys.argv[1], sys.argv[2]

# Initialize the Chrome driver (assuming Chrome is preferred)
driver = webdriver.Chrome()

# Ouverture du fichier CSV
csv_file = open('majliss.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)

try:
    # Accéder à l'URL cible
    driver.get('https://droit.mjustice.dz/ar/content/الإجتهاد-القضائي')
    driver.maximize_window()

    # Trouver et cliquer sur l'élément du menu "الإجتهاد القضائي"
    menu_xpath = "//span[contains(text(),'الإجتهاد القضائي')]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, menu_xpath))
    )
    menu_element = driver.find_element(By.XPATH, menu_xpath)
    menu_element.click()

    # Trouver et cliquer sur le premier élément dans le sous-menu (مجلس الدولة)
    submenu_xpath = "//a[contains(text(),'مجلس الدولة')]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, submenu_xpath))
    )
    submenu_element = driver.find_element(By.XPATH, submenu_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(submenu_element).perform()
    submenu_element.click()

    # Séparer les dates en jour, mois, année
    day_debut, month_debut, year_debut = date_debut.split('/')
    day_fin, month_fin, year_fin = date_fin.split('/')

    # Utiliser JavaScript pour sélectionner l'option du jour debut
    day_select_id = 'edit-field-date-arret-value-min-day'
    driver.execute_script(f"document.getElementById('{day_select_id}').value = '{day_debut}';")

    # Utiliser JavaScript pour sélectionner l'option du mois debut
    month_select_id = 'edit-field-date-arret-value-min-month'
    driver.execute_script(f"document.getElementById('{month_select_id}').value = '{month_debut}';")

    # Utiliser JavaScript pour sélectionner l'option de l'année debut
    year_select_id = 'edit-field-date-arret-value-min-year'
    driver.execute_script(f"document.getElementById('{year_select_id}').value = '{year_debut}';")

    # Utiliser JavaScript pour sélectionner l'option du jour fin
    day2_select_id = 'edit-field-date-arret-value-max-day'
    driver.execute_script(f"document.getElementById('{day2_select_id}').value = '{day_fin}';")

    # Utiliser JavaScript pour sélectionner l'option du mois fin
    month2_select_id = 'edit-field-date-arret-value-max-month'
    driver.execute_script(f"document.getElementById('{month2_select_id}').value = '{month_fin}';")

    # Utiliser JavaScript pour sélectionner l'option de l'année fin
    year2_select_id = 'edit-field-date-arret-value-max-year'
    driver.execute_script(f"document.getElementById('{year2_select_id}').value = '{year_fin}';")

    # Attendre que le bouton de recherche soit cliquable et cliquer dessus
    search_button_id = "edit-submit-jurisprudence"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, search_button_id))
    )
    search_button = driver.find_element(by=By.ID, value=search_button_id)
    search_button.click()

    current_page = 1
    while True:
        try:
            # Trouver toutes les lignes dans le tableau
            rows = driver.find_elements(By.XPATH, "//table[@class='views-table cols-8 table table-striped table-bordered table-hover table-0']/tbody/tr")
            for row in rows:
                row_data = [cell.find_element(By.XPATH, "./p").text if cell.find_elements(By.XPATH, "./p") else cell.text for cell in row.find_elements(By.XPATH, "./td")]
                writer.writerow(row_data)

            # Obtenir l'attribut href du lien de la page suivante
            next_page_href = driver.find_element(By.CSS_SELECTOR, "li.next > a").get_attribute("href")
            driver.get(next_page_href)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@class='next']")))

            logging.info(f"Page scraped")

        except NoSuchElementException:
            logging.info("Next page link not found. Assuming no more pages.")
            break

except TimeoutException:
    logging.error("Timeout occurred while waiting for the next page to load.")
finally:
    # Fermer le fichier CSV et le navigateur
    csv_file.close()
    #driver.quit()
