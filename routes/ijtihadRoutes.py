from flask import Blueprint, jsonify, request
from ..services.ijtihad import get_qrar_updated_at, get_all_qrar, get_all_qrarat_mahkama, get_details_qrarMahkama, get_all_sujets, get_unique_years, get_all_qrarat_with_details, get_details_qrarMajliss, get_all_classes, get_all_chambres, get_all_takyif, search_qrar, index_qrar
from datetime import datetime

ijtihad_routes = Blueprint('ijtihad_routes', __name__)

@ijtihad_routes.route('/qrar', methods=['GET'])
def get_all_qrar_route():
    qrar = get_all_qrar()
    serialized_qrar = []

    for q in qrar:
        serialized_q = {
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe 
            
        }
        serialized_qrar.append(serialized_q)

    return jsonify(serialized_qrar)


@ijtihad_routes.route('/qraratMahkama', methods=['GET'])
def get_all_qrarat_Mahkama_route():
    MahkamaQrar = get_all_qrarat_mahkama()
    serialized_qrarMahkama = []

    for q in MahkamaQrar:
        serialized_q = {
            'idQrarMahkama': q.idQrarMahkama,
            'refLegale': q.refLegale,
            'motsClés': q.motsClés,
            'parties': q.parties,
            'repMahkama': q.repMahkama,
            'OperatDecision': q.OperatDecision,
            'raqmQararOrigin': q.raqmQararOrigin,
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe  
        }
        serialized_qrarMahkama.append(serialized_q)

    return jsonify(serialized_qrarMahkama)


@ijtihad_routes.route('/DetailsqrarMahkama/<int:raqmQarar>', methods=['GET'])
def get_Details_qrarMahkama_route(raqmQarar):
    qrarMahkama = get_details_qrarMahkama(raqmQarar)
    
    if qrarMahkama:
        serialized_qrarMahkama = {
            'idQrarMahkama': qrarMahkama.idQrarMahkama,
            'refLegale': qrarMahkama.refLegale,
            'motsClés': qrarMahkama.motsClés,
            'parties': qrarMahkama.parties,
            'repMahkama': qrarMahkama.repMahkama,
            'OperatDecision': qrarMahkama.OperatDecision,
            'raqmQararOrigin': qrarMahkama.raqmQararOrigin,
            'raqmQarar': qrarMahkama.raqmQarar,
            'dataQarar': qrarMahkama.dataQarar,
            'sujetQarar': qrarMahkama.sujetQarar,
            'principe': qrarMahkama.principe  
        }
        return jsonify(serialized_qrarMahkama)
    else:
        return jsonify({'message': 'QrarMahkama not found'}), 404
    

@ijtihad_routes.route('/DetailsqrarMajliss/<int:raqmQarar>', methods=['GET'])
def get_details_qrarMajliss_route(raqmQarar):
    qrarMajliss = get_details_qrarMajliss(raqmQarar)
    
    if qrarMajliss:
        serialized_qrarMajliss = {
            'id_qarar_majliss': qrarMajliss.id_qarar_majliss,
            'chambre': qrarMajliss.chambre,
            'classe': qrarMajliss.classe,
            'takyif': qrarMajliss.takyif,
            'num_qarar': qrarMajliss.num_qarar,
            'raqmQarar': qrarMajliss.raqmQarar,
            'dataQarar': qrarMajliss.dataQarar,
            'sujetQarar': qrarMajliss.sujetQarar,
            'principe': qrarMajliss.principe  
        }
        return jsonify(serialized_qrarMajliss)
    else:
        return jsonify({'message': 'Majliss not found'}), 404


@ijtihad_routes.route('/sujetsQarar', methods=['GET'])
def get_all_sujets_route():
    sujets = get_all_sujets()
    serialized_sujets = []

    for sujet in sujets:
        serialized_sujet = {
            'Nomsujet': sujet.Nomsujet      
        }
        serialized_sujets.append(serialized_sujet)

    return jsonify(serialized_sujets)


@ijtihad_routes.route('/yearsQarar', methods=['GET'])
def get_unique_years_route():
    years = get_unique_years()
    serialized_years = []
    for year in years:
        serialized_year = {
            'year': year      
        }
        serialized_years.append(serialized_year)

    return jsonify(serialized_years)



@ijtihad_routes.route('/qraratwihDetails', methods=['GET'])
def get_all_qrarat_with_details_route():
    Qrarat = get_all_qrarat_with_details()
    serialized_qrarat = []

    for q in Qrarat:
        serialized_qrar = {
            'raqmQarar': q.raqmQarar,
            'dataQarar': q.dataQarar,
            'sujetQarar': q.sujetQarar,
            'principe': q.principe,
            'commission' : q.commission ,
            'مجال':q.مجال  
        }
        serialized_qrarat.append(serialized_qrar)

    return jsonify(serialized_qrarat)


@ijtihad_routes.route('/ClassesQarar', methods=['GET'])
def get_all_classes_route():
    classes = get_all_classes()
    serialized_classes = []

    for classe in classes:
        serialized_classe = {
            'Nomclasse': classe.nom_classe      
        }
        serialized_classes.append(serialized_classe)

    return jsonify(serialized_classes)


@ijtihad_routes.route('/ChambresQarar', methods=['GET'])
def get_all_chambres_route():
    chambres = get_all_chambres()
    serialized_chambres = []

    for chambre in chambres:
        serialized_chambre = {
            'NomChambre': chambre.nom_chambre      
        }
        serialized_chambres.append(serialized_chambre)

    return jsonify(serialized_chambres)



@ijtihad_routes.route('/TakyifQarar', methods=['GET'])
def get_all_takyif_route():
    takyifs = get_all_takyif()
    serialized_takyifs = []

    for takyif in takyifs:
        serialized_takyif = {
            'nom_takyif': takyif.nom_takyif      
        }
        serialized_takyifs.append(serialized_takyif)

    return jsonify(serialized_takyifs)


@ijtihad_routes.route('/searchQrar', methods=['GET'])
def search():
    query = request.args.get('q')
    index_qrar()
    results = search_qrar(query)
    return jsonify(results)




@ijtihad_routes.route('/qrars/updated-at', methods=['GET'])
def get_qrar_updated_at_route():
    datetime_str = request.args.get('datetime')
    
    if not datetime_str:
        return jsonify({"error": "Le paramètre 'datetime' est requis."}), 400
    
    try:
        datetime_param = datetime.fromisoformat(datetime_str)
    except ValueError:
        return jsonify({"error": "Le format du paramètre 'datetime' est incorrect. Utilisez le format ISO 8601."}), 400
    
    qrars_updated_at = get_qrar_updated_at(datetime_param)
    serialized_qrars = []

    for qrar in qrars_updated_at:
        serialized_qrar = {
            "raqmQarar": qrar.raqmQarar,
            "dataQarar": qrar.dataQarar.isoformat(),
            "sujetQarar": qrar.sujetQarar,
            "principe": qrar.principe,
            "updated_at": qrar.updated_at.isoformat() if qrar.updated_at else None,
            "مجال": qrar.مجال
        }
        serialized_qrars.append(serialized_qrar)

    return jsonify(serialized_qrars)