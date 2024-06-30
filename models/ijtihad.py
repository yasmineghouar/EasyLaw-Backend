from ..app import db
from sqlalchemy import func
from datetime import datetime



# Définition de la classe pour la table sujet "الموضوع"
class sujet(db.Model):
    __tablename__ = 'sujet' #الموضوع
    Nomsujet = db.Column(db.Text, primary_key=True, unique=True)

 
# Définition de la classe pour la table Qrar "قرار"
class Qrar(db.Model):
    __tablename__ = 'Qrar' 
    raqmQarar = db.Column(db.BigInteger, primary_key=True, unique=True)
    dataQarar = db.Column(db.Date, nullable=False) #date
    sujetQarar = db.Column(db.Text, db.ForeignKey('sujet.Nomsujet'), nullable=False)
    principe = db.Column(db.Text, nullable=False) #المبدأ
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    مجال = db.Column(db.String(255))

    def __repr__(self):
        return f'<Qrar {self.raqmQarar}>'


# Définition de la classe pour la table QrarMahkama "قرار_المحكمة"
class QrarMahkama(db.Model):
    __tablename__ = 'QrarMahkama'
    idQrarMahkama = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    refLegale = db.Column(db.String, nullable=False) #المرجع_القانوني
    motsClés = db.Column(db.String, nullable=False) #الكلمات_الأساسية
    parties = db.Column(db.String, nullable=False) #الأطراف
    repMahkama = db.Column(db.String, nullable=False) #رد_المحكمة_العليا
    OperatDecision = db.Column(db.String, nullable=False) #منطوق_القرار
    raqmQararOrigin = db.Column(db.Integer, db.ForeignKey('Qrar.raqmQarar'),nullable=False)

   
    def __repr__(self):
        return f'<idQrarMahkama {self.idQrarMahkama}>'


class Classe(db.Model):
    __tablename__ = 'Classe'

    nom_classe = db.Column(db.Text, primary_key=True)
   
    def __repr__(self):
        return f'<classe {self.nom_classe}>'

class Takyif(db.Model):
    __tablename__ = 'Takyif'

    nom_takyif = db.Column(db.Text, primary_key=True)
   
    def __repr__(self):
        return f'<Takyif {self.nom_takyif}>'
    
class Chambre(db.Model):
    __tablename__ = 'Chambre'

    nom_chambre = db.Column(db.Text, primary_key=True)
   
    def __repr__(self):
        return f'<Chambre {self.nom_chambre}>'

class QrarMajliss(db.Model):
    __tablename__ = 'QrarMajliss'

    id_qarar_majliss = db.Column(db.BigInteger, primary_key=True)
    chambre = db.Column(db.Text, db.ForeignKey('Chambre.nom_chambre'), nullable=True)
    classe = db.Column(db.Text, db.ForeignKey('Classe.nom_classe'), nullable=True)
    takyif  = db.Column(db.Text,db.ForeignKey('Takyif.nom_takyif') ,nullable=False)
    num_qarar  = db.Column(db.BigInteger, db.ForeignKey('Qrar.raqmQarar'),nullable=False)    