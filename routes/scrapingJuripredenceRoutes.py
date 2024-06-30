from flask import request, jsonify
from flask import Blueprint
from ..services.scrapingJuripredence import cleaningMajliss ,insertJuriMajliss, update_qrar_domain
import subprocess
import os
import logging


scrapingJuripredence_routes = Blueprint('scrapingJuripredence_routes', __name__)

@scrapingJuripredence_routes.route('/scraping-juri-majliss', methods=['GET'])
def run_scrapingJuripredence():
    datedebut = request.args.get('datedebut')
    dateEnd = request.args.get('dateEnd')
    
    if not datedebut or not dateEnd:
        return jsonify({"error": "Les paramètres 'datedebut' et 'dateEnd' sont requis."})

    try:
        subprocess.Popen(['python', 'scrapingJuripredence.py', datedebut, dateEnd])
        return jsonify({"message": "Le scraping a été déclenché avec succès."})
    except Exception as e:
        return jsonify({"error": str(e)})


@scrapingJuripredence_routes.route('/scrapeJuripredence_status', methods=['GET'])
def scrape_status():
    if os.path.exists('scrapingJuripredence.log'):
        with open('scrapingJuripredence.log', 'r') as file:
            logs = file.readlines()
            last_log = logs[-1] if logs else 'No logs found.'
            return jsonify({"status": last_log})
    return jsonify({"error": "Log file not found."})
 

@scrapingJuripredence_routes.route('/validerScraping', methods=['GET'])
def run_scraping():
    cleaning_result = cleaningMajliss()
    insertion_result = insertJuriMajliss()
    update_qrar_domain()
    return jsonify({"cleaning_result": cleaning_result, "insertion_result": insertion_result})


@scrapingJuripredence_routes.route('/indexation-qrar-domain', methods=['GET'])
def update_qrar_domain_route():
    try:
        update_qrar_domain()
        return jsonify({"message": "تم فهرسة الاجتهادات القضائية بنجاح"})
    except Exception as e:
        return jsonify({"error": str(e)})



