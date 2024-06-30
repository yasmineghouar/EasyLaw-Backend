from flask import Blueprint, jsonify, request
from ..services.tarification import update_tarification, get_tarifications_by_service_id, switch_tarification_status, get_all_tarifications_with_service_name , get_all_tarificationsAdmin , get_all_tarification_history
from ..services.user import token_required

tarification_routes = Blueprint('tarification_routes', __name__)

@tarification_routes.route('/tarification/<int:tarification_id>', methods=['PUT'])
@token_required
def update_tarification_route(current_user ,tarification_id):
    data = request.json
    return update_tarification(current_user,tarification_id, **data)

@tarification_routes.route('/tarifications/service/<int:service_id>', methods=['GET'])
def get_tarifications_by_service_id_route(service_id):
    return get_tarifications_by_service_id(service_id)

@tarification_routes.route('/tarification/switch/<int:tarification_id>', methods=['PUT'])
@token_required
def switch_tarification_status_route(current_user, tarification_id):
    return switch_tarification_status(current_user, tarification_id)

@tarification_routes.route('/tarifications', methods=['GET'])
def get_all_tarifications_with_service_name_route():
    return get_all_tarifications_with_service_name()

@tarification_routes.route('/Alltarifications', methods=['GET'])
def get_all_tarifications():
    return get_all_tarificationsAdmin()

@tarification_routes.route('/tarification-history', methods=['GET'])
def get_all_tarification_history_route():
    response, status_code = get_all_tarification_history()
    return response, status_code