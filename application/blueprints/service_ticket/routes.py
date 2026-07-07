from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from datetime import date

from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from application.extensions import db
from application.models import Service, Mechanic, Customer


@service_ticket_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.id == service_ticket_data["customer_id"])
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if isinstance(service_ticket_data["service_date"], str):
        service_ticket_data["service_date"] = date.fromisoformat(
            service_ticket_data["service_date"]
        )

    new_service_ticket = Service(**service_ticket_data)

    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_ticket_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(Service)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200

@service_ticket_bp.route("/<int:ticket_id>", methods=["GET"])
def get_service_ticket(ticket_id):
    query = select(Service).where(Service.id == ticket_id)
    service_ticket = db.session.execute(query).scalars().first()
    
    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    
    return service_ticket_schema.jsonify(service_ticket), 200


@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket_query = select(Service).where(Service.id == ticket_id)
    service_ticket = db.session.execute(ticket_query).scalars().first()

    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic_query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(mechanic_query).scalars().first()

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic in service_ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this service ticket"}), 200

    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned successfully"}), 200


@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket_query = select(Service).where(Service.id == ticket_id)
    service_ticket = db.session.execute(ticket_query).scalars().first()

    if not service_ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic_query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(mechanic_query).scalars().first()

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in service_ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this service ticket"}), 200

    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic removed successfully"}), 200