from sqlalchemy import func
from flask import request, jsonify, g, current_app
from . import mechanic_bp
from app.models import Mechanic, ServiceTicket
from app.extensions import db, limiter
from .schemas import mechanic_schema, mechanics_schema, LoginSchema

from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
import datetime
from app.utils.auth import token_required


login_schema = LoginSchema()


# ----------------------------------------------------
# TOKEN CREATION
# ----------------------------------------------------
def encode_token(mechanic_id):
    payload = {
        "sub": mechanic_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return token


# ----------------------------------------------------
# CREATE MECHANIC
# ----------------------------------------------------
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


# ----------------------------------------------------
# GET ALL MECHANICS (Rate Limited)
# ----------------------------------------------------
@limiter.limit("5/minute")
@mechanic_bp.get("/")
def get_mechanics():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = Mechanic.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page,
        "per_page": paginated.per_page,
        "items": mechanics_schema.dump(paginated.items)
    }), 200


# ----------------------------------------------------
# GET MECHANIC BY ID
# ----------------------------------------------------
@mechanic_bp.get("/<int:id>")
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(mechanic)), 200


# ----------------------------------------------------
# UPDATE MECHANIC  (Protected)
# ----------------------------------------------------
@mechanic_bp.put("/<int:id>")
@token_required
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()

    mechanic.name = data.get("name", mechanic.name)
    mechanic.email = data.get("email", mechanic.email)
    mechanic.phone = data.get("phone", mechanic.phone)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200


# ----------------------------------------------------
# DELETE MECHANIC  (Protected)
# ----------------------------------------------------
@mechanic_bp.delete("/<int:id>")
@token_required
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200


# ----------------------------------------------------
# MECHANICS ORDERED BY MOST TICKETS WORKED (Advanced Query)
# ----------------------------------------------------
@mechanic_bp.get("/most-tickets")
def mechanics_most_tickets():
    results = (
        db.session.query(
            Mechanic,
            func.count(ServiceTicket.id).label("ticket_count")
        )
        .outerjoin(Mechanic.service_tickets)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceTicket.id).desc())
        .all()
    )

    response = []
    for mechanic, count in results:
        response.append({
            "mechanic": mechanic_schema.dump(mechanic),
            "tickets_worked": count
        })

    return jsonify(response), 200


# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------
@mechanic_bp.post("/login")
def mechanic_login():
    data = request.get_json()
    creds = login_schema.load(data)

    mechanic = Mechanic.query.filter_by(email=creds["email"]).first()

    if not mechanic or not check_password_hash(mechanic.password, creds["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    token = encode_token(mechanic.id)

    return jsonify({"token": token}), 200


# ----------------------------------------------------
# MECHANIC'S OWN TICKETS (Protected)
# ----------------------------------------------------
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
            "amount_charged": t.amount_charged,
        }
        for t in tickets
    ]

    return jsonify(ticket_list), 200