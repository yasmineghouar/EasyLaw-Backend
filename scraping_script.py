import sys
import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

# Setup logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(message)s')

logging.info('Script de scraping démarré')

driver = webdriver.Chrome()


try:
    # Load the initial page
    driver.get('https://www.joradp.dz/HAR/Index.htm')

    # Maximize the window
    driver.maximize_window()

    # Wait for and switch to the first frame
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//frame[@src="ATitre.htm"]')))

    # Find and click the element inside the first frame
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div > table:nth-child(2) > tbody > tr > td:nth-child(3) > a")))
    element.click()

    # Switch back to the default content
    driver.switch_to.default_content()

    # Wait for the second frame to be available and switch to it
    frame_xpath = "/html/frameset/frameset[2]/frame[1]"
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, frame_xpath)))

    # Get dates from command line arguments
    if len(sys.argv) != 3:
        raise ValueError("Deux arguments de date sont nécessaires: datedebut et dateEnd.")
    datedebut = sys.argv[1]
    dateEnd = sys.argv[2]

    # Find input 1
    input1_css_selector = "body > div > form > table:nth-child(3) > tbody > tr:nth-child(8) > td:nth-child(2) > input[type=text]:nth-child(1)"
    input1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input1_css_selector)))

    # Find input 2
    input2_css_selector = "body > div > form > table:nth-child(3) > tbody > tr:nth-child(8) > td:nth-child(2) > input[type=text]:nth-child(2)"
    input2 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input2_css_selector)))

    # Enter values in the input elements
    input1.clear()
    input1.send_keys(datedebut)
    input2.clear()
    input2.send_keys(dateEnd)

    # Find the element with the selector '#b1 > a' and click on it
    button_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#b1 > a')))
    button_element.click()

    # Wait for the table to be available
    table_xpath = "/html/body/div/table[2]"
    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

    # Extract data from the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        cols = [col.text for col in cols]
        data.append(cols)

    while True:
        try:
            # Click on the element with the specified selector
            element_selector = "//img[@alt='الصفحة التابعة']"
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, element_selector)))
            element.click()

            # Wait for the table to be available
            table_xpath = "/html/body/div/table[2]"
            table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))

            # Extract data from the table
            rows = table.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, 'td')
                cols = [col.text for col in cols]
                data.append(cols)

            # Write data to CSV file
            with open('table_data2.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(data)

        # Find the next element and check if it exists
        except TimeoutException:
            break

        next_element_xpath = "//img[@alt='الصفحة التابعة']"
        next_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, next_element_xpath)))

except TimeoutException:
    logging.error("Timeout occurred while waiting for elements.")
except ValueError as ve:
    logging.error(f"ValueError: {ve}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    logging.info("Script de scraping terminé")
    # Quit the driver
    driver.quit()
