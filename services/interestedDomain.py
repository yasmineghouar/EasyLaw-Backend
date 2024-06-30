from flask import request, jsonify
from ..models.interestedDomain import InterestedDomain, MotsCles , InterestedDomainHistory
from ..models.law import Law 
from ..app import db
from sqlalchemy.orm import joinedload


def get_all_interested_domains():
    interested_domains = InterestedDomain.query.all()
    serialized_domains = [{"id": domain.id, "nom": domain.nom} for domain in interested_domains]
    return jsonify(serialized_domains), 200

def get_all_mots_cles(domain_id):
    mots_cles = MotsCles.query.filter_by(idInterestedDomain=domain_id).all()
    serialized_mots_cles = [{"id": mot.id, "nom": mot.nom} for mot in mots_cles]
    return jsonify(serialized_mots_cles), 200

def add_interested_domain(data, current_user):
    nom = data.get("nom")
    if nom:
        new_domain = InterestedDomain(nom=nom)
        db.session.add(new_domain)
        db.session.commit()

        history_entry = InterestedDomainHistory(
            domain_id=new_domain.id,
            action='add',
            attribute='nom',
            new_value=nom,
            changed_by=current_user.email
        )
        db.session.add(history_entry)
        db.session.commit()

        return {"message": "Interested domain name added successfully"}, 201
    return {"message": "Failed to add interested domain"}, 400



def add_mot_cle(data, domain_id, current_user):
    nom = data.get("nom")
    if nom:
        new_mot_cle = MotsCles(nom=nom, idInterestedDomain=domain_id)
        db.session.add(new_mot_cle)
        db.session.commit()

        # Ajouter l'historique
        history_entry = InterestedDomainHistory(
            domain_id=domain_id,
            action='add',
            attribute='mot_cle',
            new_value=nom,
            changed_by=current_user.email
        )
        db.session.add(history_entry)
        db.session.commit()

        return {"message": "Mot cle added successfully"}, 201
    return {"message": "Failed to add mot cle"}, 400


def update_interested_domain(data, domain_id, current_user):
    new_nom = data.get("nom")
    if new_nom:
        domain = InterestedDomain.query.get(domain_id)
        if domain:
            old_nom = domain.nom
            domain.nom = new_nom
            db.session.commit()

            # Ajouter l'historique
            history_entry = InterestedDomainHistory(
                domain_id=domain_id,
                action='update',
                attribute='nom',
                old_value=old_nom,
                new_value=new_nom,
                changed_by=current_user.email
            )
            db.session.add(history_entry)
            db.session.commit()

            return {"message": "Interested domain updated successfully"}, 200
        return {"message": "Interested domain not found"}, 404
    return {"message": "Failed to update interested domain"}, 400


def delete_mot_cle(mot_id, current_user):
    mot_cle = MotsCles.query.get(mot_id)
    if mot_cle:
        old_nom = mot_cle.nom
        db.session.delete(mot_cle)
        db.session.commit()

        # Ajouter l'historique
        history_entry = InterestedDomainHistory(
            domain_id=mot_cle.idInterestedDomain,
            action='delete',
            attribute='mot_cle',
            old_value=old_nom,
            changed_by=current_user.email
        )
        db.session.add(history_entry)
        db.session.commit()

        return {"message": "Mot cle deleted successfully"}, 200
    return {"message": "Mot cle not found"}, 404



def delete_interested_domain(domain_id, current_user):
    domain = InterestedDomain.query.get(domain_id)
    if domain:
        # Supprimer tous les mots cles associés au domaine
        mots_cles = MotsCles.query.filter_by(idInterestedDomain=domain_id).all()
        for mot_cle in mots_cles:
            old_nom = mot_cle.nom
            db.session.delete(mot_cle)

            # Ajouter l'historique pour chaque mot clé supprimé
            history_entry = InterestedDomainHistory(
                domain_id=domain_id,
                action='delete',
                attribute='mot_cle',
                old_value=old_nom,
                changed_by=current_user.username
            )
            db.session.add(history_entry)

        old_nom = domain.nom
        db.session.delete(domain)
        db.session.commit()

        # Ajouter l'historique pour le domaine
        history_entry = InterestedDomainHistory(
            domain_id=domain_id,
            action='delete',
            attribute='nom',
            old_value=old_nom,
            changed_by=current_user.username
        )
        db.session.add(history_entry)
        db.session.commit()

        return {"message": "Interested domain and associated mots cles deleted successfully"}, 200
    return {"message": "Interested domain not found"}, 404


def get_all_History_interested_domains():
    query_result = db.session.query(
        InterestedDomain.id,
        InterestedDomain.nom,
        InterestedDomainHistory.action,
        InterestedDomainHistory.attribute,
        InterestedDomainHistory.old_value,
        InterestedDomainHistory.new_value,
        InterestedDomainHistory.changed_at,
        InterestedDomainHistory.changed_by
    ).join(
        InterestedDomainHistory,
        InterestedDomain.id == InterestedDomainHistory.domain_id
    ).order_by(
        InterestedDomainHistory.changed_at.desc()
    ).all()

    # Serialize query result
    serialized_domains = []
    for domain_id, domain_nom, action, attribute, old_value, new_value, changed_at, changed_by in query_result:
        serialized_domains.append({
            "id": domain_id,
            "nom": domain_nom,
            "history": {
                "action": action,
                "attribute": attribute,
                "old_value": old_value,
                "new_value": new_value,
                "changed_at": changed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "changed_by": changed_by
            }
        })

    return jsonify(serialized_domains), 200





def update_majal_for_laws():
    domains = db.session.query(InterestedDomain).options(joinedload(InterestedDomain.mots_cles)).all()
    laws = db.session.query(Law).all()
    
    for law in laws:
        matching_domains = set()
        for domain in domains:
            for mot_cle in domain.mots_cles:
                if mot_cle.nom in law.sujet:
                    matching_domains.add(domain.nom)
                    break  # Stop checking other mots_cles once a match is found for this domain
        
        law.مجال = ", ".join(matching_domains) if matching_domains else "Non spécifié"
        db.session.add(law)
    
    db.session.commit()
