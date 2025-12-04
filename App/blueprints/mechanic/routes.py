from flask import request, jsonify, g
from . import mechanic_bp
from app.models import Mechanic, ServiceTicket
from app.extensions import db
from .schemas import mechanic_schema, mechanics_schema, LoginSchema

from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
import datetime
from flask import current_app
from app.utils.auth import token_required

login_schema = LoginSchema()


# ---- TOKEN CREATION ----

from jose import jwt

def encode_token(mechanic_id):
    payload = {
        "sub": mechanic_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return token


# CREATE mechanic
@mechanic_bp.post("/")
def create_mechanic():
    data = request.get_json()

    hashed_pw = generate_password_hash(data["password"])

    new = Mechanic(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_pw
    )

    db.session.add(new)
    db.session.commit()

    return jsonify(mechanic_schema.dump(new)), 201


# GET all mechanics
@mechanic_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics)), 200


# GET mechanic by ID
@mechanic_bp.get("/<int:id>")
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(mechanic)), 200


# UPDATE mechanic
@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()

    mechanic.name = data.get("name", mechanic.name)
    mechanic.email = data.get("email", mechanic.email)
    mechanic.phone = data.get("phone", mechanic.phone)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200


# DELETE mechanic
@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200


# LOGIN
@mechanic_bp.post("/login")
def mechanic_login():
    data = request.get_json()
    creds = login_schema.load(data)

    mechanic = Mechanic.query.filter_by(email=creds["email"]).first()

    if not mechanic:
        return jsonify({"error": "Invalid email or password"}), 401

    if not check_password_hash(mechanic.password, creds["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(mechanic.id)
     
    print("SECRET_KEY:", current_app.config["SECRET_KEY"])
 
    return jsonify({"token": token}), 200


# GET TICKETS FOR LOGGED-IN MECHANIC
@mechanic_bp.get("/my-tickets")
@token_required
def my_tickets():
    mechanic_id = g.mechanic_id

    tickets = ServiceTicket.query.filter_by(mechanic_id=mechanic_id).all()

    ticket_list = [
        {
            "id": t.id,
            "issue_description": t.issue_description,
            "amount_quoted": t.amount_quoted,
            "amount_charged": t.amount_charged
        }
        for t in tickets
    ]

    return jsonify(ticket_list), 200