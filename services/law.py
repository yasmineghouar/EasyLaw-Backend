
from flask import request
from ..models.law import  Law 
from flask import jsonify
from functools import wraps
from sqlalchemy import func
from ..app import db
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(
    ['http://localhost:9200'],  
    http_auth=('elastic', 'elastic'), 
)

def search_laws(query):
    all_results = []

   
    fields = ["sujet", "wizara", "type", "num", "num_jarida", "page_jarida","مجال"]
 
    for field in fields:
        res = es.search(index='laws', body={
            "query": {
                "match": {
                    field: query
                }
            }
        })
        all_results.extend(res['hits']['hits'])

    return [{"idLaw": hit["_id"], **hit["_source"]} for hit in all_results]


def index_laws():
    laws = Law.query.all()
    if not es.indices.exists(index='laws'):
        index_mapping = {
            "mappings": {
                "properties": {
                    "wizara": {"type": "text"},
                    "sujet": {"type": "text"},
                    "type": {"type": "text"},
                    "num": {"type": "text"},
                    "date_jarida": {"type": "text"},
                    # "date": {"type": "text"},
                    "num_jarida": {"type": "text"},                   
                    "page_jarida": {"type": "text"},
                    "مجال": {"type": "text"}
                }
            }
        }
        es.indices.create(index='laws', body=index_mapping)

    for law in laws:
        es.index(index='laws', id=law.idLaw, body={
            "wizara": law.wizara,
            "sujet": law.sujet,
            "type": law.type,
            "num": law.num,
            # "date": law.date,
            "num_jarida": law.num_jarida,
            # "date_jarida": law.date_jarida,
            "page_jarida": law.page_jarida,
            "مجال": law.مجال

        })

def filter_laws(wizara=None, law_type=None,  num_jarida=None, date_jarida=None, page_jarida=None):
    query = Law.query

    if wizara:
        query = query.filter(Law.wizara == wizara)
    if law_type:
       query = query.filter(Law.type.like(f"%{law_type}%"))
    if num_jarida:
        query = query.filter(Law.num_jarida == num_jarida)
    if date_jarida:
        query = query.filter(Law.date_jarida == date_jarida)
    if page_jarida:
        query = query.filter(Law.page_jarida == page_jarida)

    laws = query.all()
    return laws

def get_all_laws():
    laws = Law.query.all()

    return laws

def get_all_unique_wizara():
    unique_wizara = Law.query.with_entities(Law.wizara).distinct().all()
    unique_wizara = [w[0] for w in unique_wizara]  

    return unique_wizara

def get_all_laws_with_sum():
    laws = Law.query.all()

    total_sum = db.session.query(func.sum(Law.idLaw)).scalar()

    return {
        "data": laws,
        "sum": total_sum
    }

def get_law_by_id(law_id):
    law = Law.query.get(law_id)

    if law is None:
        return jsonify({'success': False, 'message': 'Law not found'}), 404

    law_json = {
        'id': law.idLaw,
        'wizara': law.wizara,
        'sujet': law.sujet,
        'type': law.type,
        'num': law.num,
        'date_jarida': law.date_jarida,
        'num_jarida': law.num_jarida,
        'page_jarida': law.page_jarida,
        'مجال':law.مجال
    }

    return jsonify({'success': True, 'law': law_json}), 200


def get_laws_updated_at(datetime_param):
    datetime_param_truncated = datetime_param.replace(microsecond=0)
    laws_updated_at = Law.query.filter(
        func.date_trunc('second', Law.updated_at) == datetime_param_truncated
    ).all()
    
    return laws_updated_at 