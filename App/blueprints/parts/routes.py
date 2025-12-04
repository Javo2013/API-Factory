from flask import jsonify
from . import parts_bp

@parts_bp.get("/")
def parts_home():
    return jsonify({"message": "Parts API placeholder"}), 200