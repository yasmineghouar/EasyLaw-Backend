from sqlalchemy import func, Enum as EnumSQL
from enum import Enum
from ..app import db

class PaymentWayEnum(Enum):
    gold_card = 'البطاقة الذهبية'
    baridi_mob = 'بريدي موب'
    cib_card = 'بطاقة السيب'

class Invoice(db.Model):
    __tablename__ = "Invoice"
    id = db.Column(db.Integer, primary_key=True)
    numFacture = db.Column(db.String(255), nullable=False, unique=True)
    dateFacture = db.Column(db.Date, nullable=False)
    prixFacture = db.Column(db.Numeric(10, 2), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    payment_Way = db.Column(db.Enum(PaymentWayEnum))
    idService = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    email = db.Column(db.String(255), default="kz_abbaci@esi.dz")
    phoneNumber = db.Column(db.String(20), default="07939921328")

    user = db.relationship("Users", backref="invoices")
    service = db.relationship("Service", backref="invoices")

    def __repr__(self):
        return f'<Invoice {self.numFacture} {self.id}>'
