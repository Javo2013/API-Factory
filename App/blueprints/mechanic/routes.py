from flask import request, jsonify
from . import mechanic_bp
from app.models import Mechanic
from app.extensions import db
from .schemas import mechanic_schema, mechanics_schema

@mechanic_bp.post("/")
def create_mechanic():
    data = request.get_json()
    new = mechanic_schema.load(data)
    db.session.add(new)
    db.session.commit()
    return jsonify(mechanic_schema.dump(new)), 201

@mechanic_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics)), 200

@mechanic_bp.get("/<int:id>")
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()

    mechanic.name = data.get("name", mechanic.name)
    mechanic.email = data.get("email", mechanic.email)
    mechanic.phone = data.get("phone", mechanic.phone)

    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200