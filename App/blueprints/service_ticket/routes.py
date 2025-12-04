from flask import request, jsonify
from . import service_ticket_bp
from app.extensions import db, cache
from app.models import ServiceTicket, Mechanic
from .schemas import service_ticket_schema, service_tickets_schema
from app.utils.auth import token_required


# ----------------------------------------------------
# CREATE SERVICE TICKET
# ----------------------------------------------------
@service_ticket_bp.post("/")
def create_ticket():
    data = request.get_json()
    ticket = service_ticket_schema.load(data)

    db.session.add(ticket)
    db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 201


# ----------------------------------------------------
# ASSIGN MECHANIC TO TICKET  (Protected)
# ----------------------------------------------------
@service_ticket_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@token_required
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200


# ----------------------------------------------------
# REMOVE MECHANIC FROM TICKET  (Protected)
# ----------------------------------------------------
@service_ticket_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
@token_required
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200


# ----------------------------------------------------
# GET ALL TICKETS  (Cached for Assignment Requirement)
# ----------------------------------------------------
@cache.cached(timeout=30)
@service_ticket_bp.get("/")
def get_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify(service_tickets_schema.dump(tickets)), 200