from ..app import db
from sqlalchemy import func
from enum import Enum
from sqlalchemy import Enum as EnumSQL

class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    nomService = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Service {self.id}>'


class DureeEnum(Enum):
    Annuelle = 'Annuelle'
    Mensuelle = 'Mensuelle'

class Tarification(db.Model):
    __tablename__ = "tarification"

    id = db.Column(db.Integer, primary_key=True)
    serviceId = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service', backref=db.backref('tarifications', lazy=True))
    duree = db.Column(EnumSQL(DureeEnum), nullable=False)
    tarif = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Tarification {self.id}>'


class TarificationHistory(db.Model):
    __tablename__ = "tarification_history"

    id = db.Column(db.Integer, primary_key=True)
    tarificationId = db.Column(db.Integer, db.ForeignKey('tarification.id'))
    tarification = db.relationship('Tarification', backref=db.backref('histories', lazy=True))
    attribute = db.Column(db.String(255))
    old_value = db.Column(db.String(255))
    new_value = db.Column(db.String(255))
    changed_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    changed_by = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<TarificationHistory {self.id}>'