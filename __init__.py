from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

app = Flask(__name__)

db= SQLAlchemy()

# Utiliser la variable d'environnement DATABASE_URL pour configurer l'URI de la base de données
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)
