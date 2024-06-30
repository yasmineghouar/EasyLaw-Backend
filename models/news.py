from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from ..app import db

class News(db.Model):
    __tablename__ = "News"
    idNews = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(255), nullable=False)
    categorie = db.Column(db.String(255), nullable=False)
    resumer = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    MotCle = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<News {self.title} {self.idNews}>'
