from flask import Blueprint, jsonify , request, make_response, send_from_directory
import os
from ..services.news import get_all_news , get_one_new , search_news , index_news

news_routes = Blueprint('news_routes', __name__)

@news_routes.route('/news', methods=['GET'])
def get_all_news_route():
    news = get_all_news()  
    serialized_news = []

    for new in news:
        serialized_news.append({
            "idNews": new.idNews,
            "title": new.title,
            "date": new.date,
            "categorie": new.categorie,
            "resumer": new.resumer,
            "detail": new.detail,
            "MotCle": new.MotCle,
            "image": new.image,
        })

    return jsonify(serialized_news)


@news_routes.route('/news/<int:id>', methods=['GET'])
def get_single_news_route(id):
    news = get_one_new(id)  
    if news:
        serialized_news = {
            "idNews": news.idNews,
            "title": news.title,
            "date": news.date,
            "categorie": news.categorie,
            "resumer": news.resumer,
            "detail": news.detail,
            "MotCle": news.MotCle,
            "image": news.image,
        }
        return jsonify(serialized_news)
    else:
        return jsonify({"message": "News not found"}), 404



@news_routes.route('/searchNews', methods=['GET'])
def search():
    query = request.args.get('q')
    index_news()
    results = search_news(query)
    return jsonify(results)
