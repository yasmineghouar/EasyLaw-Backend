# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .routes.userRoutes import user_routes 
from .routes.lawRoute import law_routes
from .routes.newsRoutes import news_routes
from .routes.ijtihadRoutes import ijtihad_routes 
from .routes.tarificationRoutes import tarification_routes
from .routes.interestedDomainRoutes import interested_domain_routes
from .routes.scrapingLaw import scrapingLaw_routes
from .routes.scrapingInfoRoute import scraping_info_routes
from .routes.scrapingJuripredenceRoutes import scrapingJuripredence_routes
from .routes.InvoiceRoute import invoices_routes
from .routes.chatbotRoute import chatbot_Routes


app.register_blueprint(user_routes, url_prefix='/')
app.register_blueprint(law_routes, url_prefix='/')
app.register_blueprint(news_routes, url_prefix='/')
app.register_blueprint(ijtihad_routes, url_prefix='/')
app.register_blueprint(tarification_routes, url_prefix='/')
app.register_blueprint(interested_domain_routes, url_prefix='/')
app.register_blueprint(scrapingLaw_routes, url_prefix='/')
app.register_blueprint(scraping_info_routes, url_prefix='/')
app.register_blueprint(scrapingJuripredence_routes, url_prefix='/')
app.register_blueprint(invoices_routes, url_prefix='/')
app.register_blueprint(chatbot_Routes, url_prefix='/')



@app.shell_context_processor
def make_shell_context():
    return {'db': db}

if __name__ == "__main__":
    app.run(debug=True)
