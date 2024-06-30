# services.py

from flask import request
from ..models.user import Users, RoleEnum
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func
from ..app import db


def signup(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    phoneNumber = data.get("phoneNumber")

    if username and email and password and role:
        user = Users.query.filter_by(email=email).first() 
        if user:
            return {"message": "Please sign in"}, 200
        user = Users(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=RoleEnum(role),
            phoneNumber=phoneNumber
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User Created"}, 201
    return {"message": "Unable to create user"}, 500

def login(auth):
    if not auth or not auth.get("password"):
        return "Proper Credentials were not provided", 401
    user = Users.query.filter_by(email=auth.get("email")).first()
    if not user:
        return "Please create an account", 401
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
            "secret",
            "HS256"
        )
        return jsonify({'token': token}), 201
    return "Please check your credentials", 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {"message": "Token is missing"}, 401
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return {"message": "Token is invalid"}, 401
        return f(current_user, *args, **kwargs)
    return decorated





def get_user_info_from_token(token):
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = data.get("id")
        if user_id:
            user = Users.query.filter_by(id=user_id).first()
            if user:
                return user
    except jwt.ExpiredSignatureError:
        return "Token has expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401
    return "User not found", 404

# ---------------------------------------------------------------------------

def add_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    phoneNumber = data.get("phoneNumber")

    if username and email and password and role:
        user = Users.query.filter_by(email=email).first()
        if user:
            return {"message": "Email already exists"}, 400
        user = Users(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=RoleEnum(role),
            phoneNumber=phoneNumber
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User Created"}, 201
    return {"message": "Unable to create user"}, 500

def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user:
        user.deleted = True
        db.session.commit()
        return {"message": "User marked as deleted"}, 200
    return {"message": "User not found"}, 404

def validate_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user:
        user.deleted = False
        db.session.commit()
        return {"message": "User validated"}, 200
    return {"message": "User not found"}, 404

def get_moderators():
    moderators = Users.query.filter_by(role=RoleEnum.moderateur).all()
    serialized_moderators = [{"id": moderator.id, "username": moderator.username, "email": moderator.email ,"deleted": moderator.deleted ,"phoneNumber":moderator.phoneNumber} for moderator in moderators]
    return {"moderators": serialized_moderators}, 200

def get_users():
    users = Users.query.filter_by(role=RoleEnum.user).all()
    serialized_users = [{"id": user.id, "username": user.username, "email": user.email,"deleted": user.deleted ,"phoneNumber":user.phoneNumber } for user in users]
    return {"users": serialized_users}, 200


def update_user(user_id, data):
    user = Users.query.get_or_404(user_id)

    # Vérifier si les champs existent dans les données
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'phoneNumber' in data:
        user.phoneNumber = data['phoneNumber']

    # Enregistrer les modifications dans la base de données
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print("Failed to update user:", str(e))
        return False
