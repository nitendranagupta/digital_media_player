from flask import Blueprint, request
from models import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__)

@auth.post("/register")
def register():
    data = request.json
    hashed = generate_password_hash(data["password"])

    user = User(name=data["name"], email=data["email"], password=hashed)
    db.session.add(user)
    db.session.commit()

    return {"message": "User registered"}

@auth.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))

    return {"token": token}
