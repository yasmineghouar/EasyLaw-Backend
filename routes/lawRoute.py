from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
from datetime import datetime
from ..services.law import get_all_laws , get_all_unique_wizara, search_laws , index_laws ,filter_laws,get_law_by_id , get_laws_updated_at
law_routes = Blueprint('law_routes', __name__)

@law_routes.route('/laws', methods=['GET'])
def get_all_laws_route():
    laws = get_all_laws()  
    serialized_laws = []

    for law in laws:
        serialized_law = {
            "idLaw": law.idLaw,
            "wizara": law.wizara,
            "sujet": law.sujet,
            "type": law.type,
            "num": law.num,
            "date": law.date,
            "num_jarida": law.num_jarida,
            "date_jarida": law.date_jarida,
            "page_jarida": law.page_jarida ,
            "مجال": law.مجال
        }
        serialized_laws.append(serialized_law)

    return jsonify(serialized_laws)


@law_routes.route('/laws/wizara', methods=['GET'])  
def get_unique_wizara_route():
    unique_wizara = get_all_unique_wizara()  
    return jsonify(unique_wizara)  

UPLOAD_FOLDER = 'uploads'  
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@law_routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Aucun fichier trouvé', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'Nom de fichier vide', 400
    
    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'Fichier téléchargé avec succès', 200

@law_routes.route('/upload/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

 
@law_routes.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    index_laws()
    results = search_laws(query)
    return jsonify(results)

@law_routes.route('/filtered-laws', methods=['GET'])
def get_filtered_laws():
    wizara = request.args.get('wizara')
    law_type = request.args.get('law_type')
    num_jarida = request.args.get('num_jarida')
    date_jarida = request.args.get('date_jarida')
    page_jarida = request.args.get('page_jarida')

    filtered_laws = filter_laws(wizara, law_type, num_jarida, date_jarida, page_jarida)

    laws_json = [{'idLaw': law.idLaw, 'wizara': law.wizara, 'type': law.type, 'num_jarida': law.num_jarida, 'date_jarida': law.date_jarida, 'page_jarida': law.page_jarida} for law in filtered_laws]

    return jsonify({'filtered_laws': laws_json})



@law_routes.route('/law/<int:law_id>', methods=['GET'])
def get_law(law_id):
    return  get_law_by_id(law_id)
    

@law_routes.route('/laws/updated-at', methods=['GET'])
def get_laws_updated_at_route():
    datetime_str = request.args.get('datetime')
    datetime_param = datetime.fromisoformat(datetime_str)
    laws_updated_at = get_laws_updated_at(datetime_param)
    serialized_laws = []

    for law in laws_updated_at:
        serialized_law = {
            "idLaw": law.idLaw, 
            "wizara": law.wizara,
            "sujet": law.sujet,
            "type": law.type,
            "num": law.num,
            "date": law.date,
            "num_jarida": law.num_jarida,
            "date_jarida": law.date_jarida,
            "page_jarida": law.page_jarida ,
            "مجال": law.مجال
        }
        serialized_laws.append(serialized_law)

    return jsonify(serialized_laws)
    