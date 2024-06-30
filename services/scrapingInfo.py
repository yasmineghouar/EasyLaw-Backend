from flask import request, jsonify
from ..models.ScrapingInfo import ScrapingInfo  , ScrapingInfoHistory
from ..app import db
from datetime import datetime
 

def get_scraping_info():
    try:
        scraping_info_list = ScrapingInfo.query.all()
        
        scraping_info_data = []
        for info in scraping_info_list:
            scraping_info_data.append({
                "id": info.id,
                "service": info.service,
                "lastDate": info.lastDate.isoformat() if info.lastDate else None
            })
        
        return jsonify(scraping_info_data), 200
    except Exception as e:
        print("Erreur lors de la récupération des informations de scraping:", str(e))
        return jsonify({"message": "An error occurred", "error": str(e)}), 500



def update_scraping_info(scraping_info_id, data, updated_by="عباسي تسنيم"):
    try:
        # Récupérer l'information de scraping
        scraping_info = ScrapingInfo.query.get(scraping_info_id)
        if not scraping_info:
            return {"message": "Scraping info not found"}, 404

        # Déterminer le service basé sur l'ID
        if scraping_info_id == 1:
            service = "قوانين الجريدة الرسمية"
        elif scraping_info_id == 2:
            service = "اجتهادات قضائية"
        elif scraping_info_id == 3:
            service = "وثائق"
        else:
            service = "Unknown"

        # Mettre à jour la date de scraping
        updated_at = data.get("lastDate")
        scraping_info.lastDate = updated_at

        # Créer une entrée dans l'historique
        history_entry = ScrapingInfoHistory(
            scraping_info_id=scraping_info_id,
            updated_at=updated_at,
            service=service,
            action="تجريف",
            updated_by=updated_by
        )
        db.session.add(history_entry)
        
        # Ajouter la mise à jour de scraping_info à la session
        db.session.add(scraping_info)
        
        # Valider la session
        db.session.commit()

        return jsonify({"message": "Scraping info updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def toggle_autoScraping(scraping_info_id, user_email):
    try:
        scraping_info = ScrapingInfo.query.get(scraping_info_id)
        if not scraping_info:
            return jsonify({"message": "Scraping info not found"}), 404

        old_autoScraping = scraping_info.autoScraping
        scraping_info.autoScraping = not scraping_info.autoScraping
        
        if scraping_info_id == 1:
            service = "قوانين اساسية"
        elif scraping_info_id == 2:
            service = "اجتهادات قضائية"
        elif scraping_info_id == 3:
            service = "وثائق"
        else:
            service = "Unknown"


        history_entry = ScrapingInfoHistory(
            scraping_info_id=scraping_info_id,
            autoScraping=scraping_info.autoScraping,
            service = service ,
            action = "تغيير الية التجريف" ,
            updated_by=user_email 
        )
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({"message": "autoScraping state toggled successfully", "autoScraping": scraping_info.autoScraping}), 200
    except Exception as e:
        db.session.rollback()  # Revenir sur les changements en cas d'erreur
        return jsonify({"message": "An error occurred", "error": str(e)}), 500



def get_scraping_info_history():
    try:
        history_entries = ScrapingInfoHistory.query.all()
        history_data = []
        for entry in history_entries:
            history_data.append({
                "id": entry.id,
                "scraping_info_id": entry.scraping_info_id,
                "service": entry.service,
                "autoScraping": entry.autoScraping,
                "lastDate": entry.lastDate,
                "updated_at": entry.updated_at,
                "updated_by": entry.updated_by,
                "action": entry.action
            })

        return history_data
    except Exception as e:
        print("An error occurred while retrieving scraping info history:", str(e))
        return []