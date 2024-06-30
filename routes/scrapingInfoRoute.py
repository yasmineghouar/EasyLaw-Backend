from flask import Blueprint, request, make_response, jsonify
from ..services.scrapingInfo import update_scraping_info  , toggle_autoScraping , get_scraping_info , get_scraping_info_history
from ..models.user import Users
from ..services.user import token_required

scraping_info_routes = Blueprint('scraping_info_routes', __name__)

@scraping_info_routes.route("/scraping-info/<int:scraping_info_id>", methods=["PUT"])
def update_scraping_info_route(scraping_info_id):
    data = request.json
    print(data) 
    response, status_code = update_scraping_info(scraping_info_id, data)
    return make_response(response, status_code)


@scraping_info_routes.route('/toggle_autoScraping/<int:scraping_info_id>', methods=['POST'])
def toggle_autoScraping_route(scraping_info_id):
    user_email = request.json.get("user_email", None)
    if not user_email:
        return jsonify({"message": "User email not provided"}), 400

    return toggle_autoScraping(scraping_info_id, user_email)


@scraping_info_routes.route('/scraping-info', methods=['GET'])
def get_scraping_info_route():
    return get_scraping_info() 


@scraping_info_routes.route("/scraping-info-history", methods=["GET"])
def get_scraping_info_history_route():
    history_data = get_scraping_info_history()
    return jsonify(history_data)    