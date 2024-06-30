from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
from ..services.Invoice import get_all_invoices_by_user_id ,get_invoice_by_id

invoices_routes = Blueprint('invoices_routes', __name__)


@invoices_routes.route("/invoices/<int:user_id>", methods=["GET"])
def get_invoices_by_user_route(user_id):
    response = get_all_invoices_by_user_id(user_id)
    return make_response(response)


@invoices_routes.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    return get_invoice_by_id(invoice_id)