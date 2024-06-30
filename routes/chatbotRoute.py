from flask import Blueprint, jsonify, request
from configparser import ConfigParser
import cohere
from pinecone import Pinecone
from cohere.errors import BadRequestError

from ..services.chatbotService import cohere_specialized_call

# Create a blueprint
chatbot_Routes = Blueprint('chatbot', __name__)

@chatbot_Routes.route('/chatbot', methods=['POST'])
def query():
    try:
        data = request.json
        message = data.get('message')
        if not message:
            return jsonify({"error": "Message is required"}), 400
        result = cohere_specialized_call(message)
        print("result", result)
        return jsonify({"response": result}), 200
    except BadRequestError as e:
        return jsonify({"error": str(e)}), 400
