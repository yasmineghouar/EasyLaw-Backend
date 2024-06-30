from flask import Blueprint, request, make_response, jsonify
from ..services.interestedDomain import (
    get_all_interested_domains,
    get_all_mots_cles,
    add_interested_domain,
    add_mot_cle,
    update_interested_domain,
    delete_mot_cle,
    delete_interested_domain ,
    get_all_History_interested_domains ,
    update_majal_for_laws
)
from ..services.user import token_required

interested_domain_routes = Blueprint('interested_domain_routes', __name__)

@interested_domain_routes.route('/interested-domains', methods=['GET'])
def get_all_interested_domains_route():
    return get_all_interested_domains()

@interested_domain_routes.route('/interested-domain/<int:domain_id>/mots-cles', methods=['GET'])
def get_all_mots_cles_route(domain_id):
    return get_all_mots_cles(domain_id)

@interested_domain_routes.route('/interested-domain', methods=['POST'])
@token_required
def add_interested_domain_route(current_user):
    data = request.json
    return add_interested_domain(data, current_user)

@interested_domain_routes.route('/interested-domain/<int:domain_id>/mot-cle', methods=['POST'])
@token_required
def add_mot_cle_route(current_user, domain_id):
    data = request.json
    return add_mot_cle(data, domain_id, current_user)

@interested_domain_routes.route('/interested-domain/<int:domain_id>', methods=['PUT'])
def update_interested_domain_route(current_user, domain_id):
    data = request.json
    return update_interested_domain(data, domain_id, current_user)

@interested_domain_routes.route('/mot-cle/<int:mot_id>', methods=['DELETE'])
def delete_mot_cle_route(current_user, mot_id):
    return delete_mot_cle(mot_id, current_user)

@interested_domain_routes.route('/interested-domain/<int:domain_id>', methods=['DELETE'])
@token_required
def delete_interested_domain_route(current_user, domain_id):
    return delete_interested_domain(domain_id, current_user)


 
@interested_domain_routes.route('/History_interested-domains', methods=['GET'])
def get_all_history_interested_domains_route():
    return get_all_History_interested_domains()


@interested_domain_routes.route('/update-majal', methods=['GET'])
def update_majal():
    try:
        update_majal_for_laws()
        return jsonify({'message': 'تم فهرسة قوانين الجريدة الرسمية بنجاح'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500