
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)


# -------------------------
# USER REGISTRATION
# -------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"errors": ["Request body must be a valid JSON object"]}, 400

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    # Validate data types
    if not isinstance(username, str):
        return {"errors": ["Username must be a string"]}, 400

    if not isinstance(password, str):
        return {"errors": ["Password must be a string"]}, 400

    if not isinstance(password_confirmation, str):
        return {"errors": ["Password confirmation must be a string"]}, 400

    # Remove unnecessary whitespace from username
    username = username.strip()
    # Validate required fields
    if not username or not password or not password_confirmation:
        return {"errors": ["All fields are required"]}, 400

    if password != password_confirmation:
        return {"errors": ["Passwords do not match"]}, 400

    if len(password) < 8:
        return {"errors": ["Password must be at least 8 characters"]}, 400

    # Check whether username already exists
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"errors": ["Username already exists"]}, 409

    # Create and save user
    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Generate JWT
    access_token = create_access_token(identity=str(user.id))

    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 201


# -------------------------
# USER LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"errors": ["Request body must be a valid JSON object"]}, 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str):
        return {"errors": ["Username must be a string"]}, 400

    if not isinstance(password, str):
        return {"errors": ["Password must be a string"]}, 400

    username = username.strip()
    if not username or not password:
        return {"errors": ["Username and password are required"]}, 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return {"errors": ["Invalid username or password"]}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200


# -------------------------
# CURRENT USER PROFILE
# -------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return {"errors": ["User not found"]}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200
