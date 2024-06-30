from flask import jsonify
from ..models.Invoice import Invoice
from ..models.user import Users
from ..models.tarification import Service
from ..app import db

def get_all_invoices_by_user_id(user_id):
    invoices = Invoice.query.filter_by(idUser=user_id).all()
    if not invoices:
        return jsonify({"message": "No invoices found for this user"}), 404

    serialized_invoices = [
        {
            "numFacture": invoice.numFacture,
            "dateFacture": invoice.dateFacture,
            "prixFacture": invoice.prixFacture,
            "payment_Way": invoice.payment_Way.value,
            "idService": invoice.idService,
            "email": invoice.email,
            "phoneNumber": invoice.phoneNumber,
            "id":invoice.id
        }
        for invoice in invoices
    ]
    
    return jsonify({"invoices": serialized_invoices}), 200


def get_invoice_by_id(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({"message": "Invoice not found"}), 404

    user = Users.query.get(invoice.idUser)
    service = Service.query.get(invoice.idService)

    if not user or not service:
        return jsonify({"message": "User or Service not found"}), 404

    invoice_info = {
        "numFacture": invoice.numFacture,
        "dateFacture": invoice.dateFacture,
        "prixFacture": invoice.prixFacture,
        "payment_Way": invoice.payment_Way.value,
        "email": invoice.email,
        "phoneNumber": invoice.phoneNumber,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phoneNumber": user.phoneNumber,
            "role": user.role.value
        },
        "service": {
            "id": service.id,
            "nomService": service.nomService,
            "description": service.description
        }
    }
    
    return jsonify({"invoice": invoice_info}), 200