from flask import jsonify
from ..models.tarification import Tarification, Service , TarificationHistory
from ..app import db
from .user import token_required

def update_tarification(current_user, tarification_id, **kwargs):
    tarification = Tarification.query.get(tarification_id)
    if not tarification:
        return jsonify({'success': False, 'message': 'Tarification not found'}), 404

    for key, value in kwargs.items():
        if key != 'active':
            old_value = getattr(tarification, key)
            if old_value != value:
                history_entry = TarificationHistory(
                    tarificationId=tarification_id,
                    attribute=key,
                    old_value=str(old_value),
                    new_value=str(value),
                    changed_by=current_user.email  # Assurez-vous que `current_user` a un attribut `username`
                )
                db.session.add(history_entry)
                setattr(tarification, key, value)

    db.session.commit()

    return jsonify({'success': True, 'message': 'Tarification updated successfully'}), 200



def get_tarifications_by_service_id(service_id):
    tarifications = Tarification.query.filter_by(serviceId=service_id).all()

    if not tarifications:
        return jsonify({'success': False, 'message': 'No tarifications found for this service'}), 404

    tarifications_json = [{
        'id': tarif.id,
        'serviceId': tarif.serviceId,
        'duree': tarif.duree.value ,
        'tarif': tarif.tarif,
        'description': tarif.description,
        'active': tarif.active
    } for tarif in tarifications]

    return jsonify({'success': True, 'tarifications': tarifications_json}), 200


def switch_tarification_status(current_user, tarification_id):
    # Vérifie si la tarification existe
    tarification = Tarification.query.get(tarification_id)
    if not tarification:
        return jsonify({'success': False, 'message': 'Tarification not found'}), 404

    # Ajouter un enregistrement à l'historique avant de changer l'état de la tarification
    history_entry = TarificationHistory(
        tarificationId=tarification_id,
        attribute='active',
        old_value=str(tarification.active),
        new_value=str(not tarification.active),
        changed_by=current_user.email
    )
    db.session.add(history_entry)

    # Inverser l'état de l'attribut 'active'
    tarification.active = not tarification.active
    db.session.commit()

    return jsonify({'success': True, 'message': 'Tarification status updated successfully'}), 200



def get_all_tarifications_with_service_name():
    # Jointure pour obtenir les tarifications avec les détails du service associé
    tarifications = db.session.query(Tarification, Service).join(Service, Tarification.serviceId == Service.id).filter(Tarification.active == True).all()

    if not tarifications:
        return jsonify({'success': False, 'message': 'No tarifications found'}), 404

    tarifications_json = [{
        'id': tarif.id,
        'serviceId': tarif.serviceId,
        'serviceName': service.nomService,
        'duree': tarif.duree.value,
        'tarif': tarif.tarif,
        'description': tarif.description,
        'active': tarif.active
    } for tarif, service in tarifications]

    return jsonify({'success': True, 'tarifications': tarifications_json}), 200


def get_all_tarificationsAdmin():
    # Jointure pour obtenir les tarifications avec les détails du service associé
    tarifications = db.session.query(Tarification, Service).join(Service, Tarification.serviceId == Service.id).all()

    if not tarifications:
        return jsonify({'success': False, 'message': 'No tarifications found'}), 404

    tarifications_json = [{
        'id': tarif.id,
        'serviceId': tarif.serviceId,
        'serviceName': service.nomService,
        'duree': tarif.duree.value,
        'tarif': tarif.tarif,
        'description': tarif.description,
        'active': tarif.active
    } for tarif, service in tarifications]

    return jsonify({'success': True, 'tarifications': tarifications_json}), 200



def get_all_tarification_history():
    try:
        # Order by changed_at in descending order
        history_entries = TarificationHistory.query.order_by(TarificationHistory.changed_at.desc()).all()
        if not history_entries:
            return jsonify({"message": "No history found"}), 404

        history_data = []
        for entry in history_entries:
            tarification = Tarification.query.get(entry.tarificationId)
            if tarification:
                tarification_info = {
                    "tarificationId": tarification.id,
                    "serviceId": tarification.serviceId,
                    "service": tarification.service.nomService,
                    "duree": tarification.duree.value,
                    "tarif": tarification.tarif,
                    "description": tarification.description,
                    "active": tarification.active,
                    "created_at": tarification.created_at
                }
            else:
                tarification_info = None

            history_data.append({
                "id": entry.id,
                "tarificationId": entry.tarificationId,
                "attribute": entry.attribute,
                "old_value": entry.old_value,
                "new_value": entry.new_value,
                "changed_at": entry.changed_at,
                "changed_by": entry.changed_by,
                "tarification_info": tarification_info
            })

        return jsonify(history_data), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
