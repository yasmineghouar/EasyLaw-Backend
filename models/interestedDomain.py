from ..app import db
from sqlalchemy import func

class InterestedDomain(db.Model):
    __tablename__ = "interestedDomain"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    mots_cles = db.relationship("MotsCles", backref="interested_domain", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<InterestedDomain {self.nom} {self.id}>'

class MotsCles(db.Model):
    __tablename__ = "motsCles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    idInterestedDomain = db.Column(db.Integer, db.ForeignKey("interestedDomain.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f'<MotsCles {self.nom} {self.id}>' 
 

class InterestedDomainHistory(db.Model):
    __tablename__ = "interested_domain_history"

    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer)
    action = db.Column(db.String(50))
    attribute = db.Column(db.String(50))
    old_value = db.Column(db.String(255))
    new_value = db.Column(db.String(255))
    changed_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    changed_by = db.Column(db.String(255))

    def __repr__(self):
        return f'<InterestedDomainHistory {self.id}>'
    