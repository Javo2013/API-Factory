from flask import request, jsonify
from . import parts_bp
from app.extensions import db
from app.models import Inventory
from .schemas import inventory_schema, inventories_schema
from app.utils.auth import token_required


# ----------------------------------------------------
# CREATE PART
# ----------------------------------------------------
@parts_bp.post("/")
@token_required
def create_part():
    data = request.get_json()

    new_part = Inventory(
        name=data["name"],
        price=data["price"]
    )
    db.session.add(new_part)
    db.session.commit()

    return jsonify(inventory_schema.dump(new_part)), 201


# ----------------------------------------------------
# GET ALL PARTS
# ----------------------------------------------------
@parts_bp.get("/")
def get_parts():
    parts = Inventory.query.all()
    return jsonify(inventories_schema.dump(parts)), 200


# ----------------------------------------------------
# GET SINGLE PART
# ----------------------------------------------------
@parts_bp.get("/<int:id>")
def get_part(id):
    part = Inventory.query.get_or_404(id)
    return jsonify(inventory_schema.dump(part)), 200


# ----------------------------------------------------
# UPDATE PART
# ----------------------------------------------------
@parts_bp.put("/<int:id>")
@token_required
def update_part(id):
    part = Inventory.query.get_or_404(id)
    data = request.get_json()

    part.name = data.get("name", part.name)
    part.price = data.get("price", part.price)

    db.session.commit()
    return jsonify(inventory_schema.dump(part)), 200


# ----------------------------------------------------
# DELETE PART
# ----------------------------------------------------
@parts_bp.delete("/<int:id>")
@token_required
def delete_part(id):
    part = Inventory.query.get_or_404(id)
    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": "Part deleted"}), 200