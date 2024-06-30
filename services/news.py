from flask import request
from ..models.news import  News
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
# import jwt
# from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from ..app import db
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://localhost:9200'],  # Include the port in the host URL
    http_auth=('elastic', 'elastic'), 
)
def search_news(query):
    all_results = []

    fields = ["title", "resumer"]

    for field in fields:
        res = es.search(index='news', body={
            "query": {
                "match": {
                    field: query
                }
            }
        })
        # Ajouter les résultats à la liste
        all_results.extend(res['hits']['hits'])

    # Retourner les résultats avec l'identifiant de la loi inclus
    return [{"idNews": hit["_id"], **hit["_source"]} for hit in all_results]


def index_news():
    news = News.query.all()
    # Check if the 'laws' index exists
    if not es.indices.exists(index='news'):
        # Define the index mapping
        index_mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "resumer": {"type": "text"}
                }
            }
        }
        # Create the 'laws' index with the defined mapping
        es.indices.create(index='news', body=index_mapping)

    # Index each law into Elasticsearch
    for new in news:
        es.index(index='news', id=new.idNews, body={
            "title": new.title,
            "resumer": new.resumer
        })



def get_all_news():
    news = News.query.all()
    return news

def get_one_new(id):
    new = News.query.filter_by(idNews=id).first()
    return new