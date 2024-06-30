from flask import request, jsonify
from ..services.scrapingLaw import  process_data, add_domains, insert_data , is_file_empty 
from flask import Blueprint
from ..services.law import get_all_laws 
import subprocess
import os
import logging


scrapingLaw_routes = Blueprint('scrapingLaw_routes', __name__)

@scrapingLaw_routes.route('/scrape', methods=['GET'])
def run_scraping(): 
    datedebut = request.args.get('datedebut')
    dateEnd = request.args.get('dateEnd')
     
    if not datedebut or not dateEnd:
        return jsonify({"error": "Les paramètres 'datedebut' et 'dateEnd' sont requis."})
    try:
        subprocess.Popen(['python', 'scraping_script.py', datedebut, dateEnd])
        return jsonify({"message": "Le scraping a été déclenché avec succès."})
    except Exception as e:
        return jsonify({"error": str(e)})


@scrapingLaw_routes.route('/scrape_status', methods=['GET'])
def scrape_status():
    if os.path.exists('scraping.log'):
        with open('scraping.log', 'r') as file:
            logs = file.readlines()
            last_log = logs[-1] if logs else 'No logs found.'
            return jsonify({"status": last_log})
    return jsonify({"error": "Log file not found."})


@scrapingLaw_routes.route('/process', methods=['GET'])
def process_data_route():
    try:
        process_data()
        add_domains()

        return jsonify({"message": "Le traitement des données est terminé avec succès."})
    except Exception as e:
        return jsonify({"error": str(e)})    


@scrapingLaw_routes.route('/check_file_empty', methods=['GET'])
def check_file_empty():
    filename = "structured_data_avec_domaines.csv"
    file_empty = is_file_empty(filename)
    
    if file_empty:
        return jsonify({"message": "The file is empty"}), 200
    else:
        return jsonify({"message": "The file is not empty"}), 200



@scrapingLaw_routes.route('/confirmScraping', methods=['GET'])
def confirmScraping():
    insert_data()
    return jsonify({"message": "confirm scraping"})
    