from sqlalchemy import func
from datetime import datetime
from ..app import db

class Law(db.Model):
    __tablename__ = "law"

    idLaw = db.Column(db.Integer, primary_key=True , autoincrement=True)
    wizara = db.Column(db.String(255))
    sujet = db.Column(db.Text)
    type = db.Column(db.String(255))
    num = db.Column(db.String(255))
    date = db.Column(db.String(255))
    num_jarida = db.Column(db.Integer)
    date_jarida = db.Column(db.String(255))
    page_jarida = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    مجال = db.Column(db.String(255))
    def __repr__(self):
        return f'<Law {self.idLaw}>'
    


