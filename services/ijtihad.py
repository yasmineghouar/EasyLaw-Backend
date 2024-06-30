from flask import request
from ..models.ijtihad import Qrar, QrarMahkama, sujet, QrarMajliss, Classe, Chambre, Takyif
from flask import jsonify
from functools import wraps
from sqlalchemy import func, literal
from ..app import db
from elasticsearch import Elasticsearch


try:
    es = Elasticsearch(
        ['http://localhost:9200'],  # Include the port in the host URL
        http_auth=('elastic','elastic'),  
    )
except Exception as e:
    print("Erreur lors de la connexion à Elasticsearch:", e)

def get_all_qrar():
    qrar = Qrar.query.all()
    return qrar 


def get_all_qrarat_mahkama():
    qrarat_mahkama = db.session.query(
        QrarMahkama.idQrarMahkama,  
        QrarMahkama.refLegale,
        QrarMahkama.motsClés,
        QrarMahkama.parties,
        QrarMahkama.repMahkama,
        QrarMahkama.OperatDecision,
        QrarMahkama.raqmQararOrigin,
        Qrar.raqmQarar,  
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).all()

    return qrarat_mahkama

def get_all_qrarat_majliss():
    qrarat_majliss = db.session.query(
        QrarMajliss.id_qarar_majliss,
        QrarMajliss.chambre,
        QrarMajliss.classe,
        QrarMajliss.takyif,
        QrarMajliss.num_qarar,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe,
    ).join(
        QrarMajliss, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).all()

    return qrarat_majliss

##################################################################################
def get_all_qrarat_with_details():

    qrarat_with_details_1 = db.session.query(
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe,
        Qrar.مجال,
        literal("المحكمة العليا").label("commission")   
    ).join(
        QrarMahkama, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).all()
    #  jointure entre QrarMahkama et Qrar
    qrarat_with_details_2 = db.session.query(
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe,
        Qrar.مجال,
        literal("مجلس الدولة").label("commission") 
    ).join(
        QrarMajliss, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).all()

    # Fusionner les résultats des deux jointures
    qrarat_with_details = qrarat_with_details_1 + qrarat_with_details_2
    # Mélanger les éléments de la liste
    # shuffle(qrarat_with_details)

    return qrarat_with_details


##################################################################################

def get_details_qrarMahkama(raqmQarar):
    qrar_mahkama = db.session.query(
        QrarMahkama.idQrarMahkama,
        QrarMahkama.refLegale,
        QrarMahkama.motsClés,
        QrarMahkama.parties,
        QrarMahkama.repMahkama,
        QrarMahkama.OperatDecision,
        QrarMahkama.raqmQararOrigin,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMahkama.raqmQararOrigin == Qrar.raqmQarar
    ).filter(Qrar.raqmQarar == raqmQarar).first()
    return qrar_mahkama


def get_details_qrarMajliss(raqmQarar):
    qrar_majliss = db.session.query(
        QrarMajliss.id_qarar_majliss,
        QrarMajliss.chambre,
        QrarMajliss.classe,
        QrarMajliss.takyif,
        QrarMajliss.num_qarar,
        Qrar.raqmQarar,
        Qrar.dataQarar,
        Qrar.sujetQarar,
        Qrar.principe
    ).join(
        Qrar, QrarMajliss.num_qarar == Qrar.raqmQarar
    ).filter(Qrar.raqmQarar == raqmQarar).first()
    return qrar_majliss


def get_all_sujets():
    sujets = sujet.query.all()
    return sujets

def get_unique_years():
    unique_years = db.session.query(func.extract('year', Qrar.dataQarar)).distinct().all()
    years = [year[0] for year in unique_years if year[0] is not None]  # Filter les valeurs vides
    return years

def get_all_classes():
    classes = Classe.query.all()
    return classes

def get_all_chambres():
    chambres = Chambre.query.all()
    return chambres


def get_all_takyif():
    takyifs = Takyif.query.all()
    return takyifs

def search_qrar(query):
    # Initialiser une liste pour stocker les résultats
    all_results = []

    # Liste des champs sur lesquels effectuer la recherche
    fields = [ "sujetQarar","principe"]

    # Effectuer une recherche pour chaque champ
    for field in fields:
        res = es.search(index='qrar', body={
            "query": {
                "match": {
                    field: query
                }
            }
        })
        # Ajouter les résultats à la liste
        all_results.extend(res['hits']['hits'])

    # Retourner les résultats avec l'identifiant de la loi inclus
    return [{"raqmQarar": hit["_id"], **hit["_source"]} for hit in all_results]

def index_qrar():
    qrars = Qrar.query.all()
    if not es.indices.exists(index='qrar'):
        index_mapping = {
            "mappings": {
                "properties": {
                    "sujetQarar": {"type": "text"},
                    "principe": {"type": "text"},
                    # "dataQarar": {"type": "date"},
                }
            }
        }
        es.indices.create(index='qrar', body=index_mapping)

    for qrar in qrars:
        es.index(index='qrar', id=qrar.raqmQarar, body={
            "sujetQarar": qrar.sujetQarar,
            "principe": qrar.principe,
            "dataQarar": qrar.dataQarar,
            "مجال": qrar.مجال 
        })


def get_qrar_updated_at(datetime_param):
    datetime_param_truncated = datetime_param.replace(microsecond=0)
    qrar_updated_at = Qrar.query.filter(
        func.date_trunc('second', Qrar.updated_at) == datetime_param_truncated
    ).all()
    
    return qrar_updated_at 
