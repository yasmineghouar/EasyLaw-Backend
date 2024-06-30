from sqlalchemy import func
from enum import Enum
from sqlalchemy import Enum as EnumSQL
from ..app import db


class RoleEnum(Enum):
    user = 'user'
    admin = 'admin'
    moderateur = 'moderateur'

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    phoneNumber = db.Column(db.String(20))
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.username} {self.id}>'


