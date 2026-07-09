from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func

from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from application.extensions import db
from application.models import Mechanic, Service, service_mechanics
from application.utils import encode_mechanic_token, mechanic_token_required

#CREATE new mechanic
@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data["email"])
    existing_mechanic = db.session.execute(query).scalars().first()
    
    if existing_mechanic:
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    
    db.session.add(new_mechanic)
    db.session.commit()
    
    return mechanic_schema.jsonify(new_mechanic), 201

#READ all mechanics
@mechanic_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics), 200

#READ one mechanic
@mechanic_bp.route("/<int:id>", methods=["GET"])
def get_mechanic(id):
    query = select(Mechanic).where(Mechanic.id == id)
    mechanic = db.session.execute(query).scalars().first()
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    return mechanic_schema.jsonify(mechanic), 200

#UPDATE mechanic
@mechanic_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    query = select(Mechanic).where(Mechanic.id == id)
    mechanic = db.session.execute(query).scalars().first()
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    if "email" in mechanic_data:
        query = select(Mechanic).where(Mechanic.email == mechanic_data["email"])
        existing_mechanic = db.session.execute(query).scalars().first()
        
        if existing_mechanic and existing_mechanic.id != mechanic.id:
            return jsonify({"error": "Email already associated with a mechanic"}), 400
        
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    
    return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    query = select(Mechanic).where(Mechanic.id == id)
    mechanic = db.session.execute(query).scalars().first()
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    mechanic.services.clear()
    
    db.session.delete(mechanic)
    db.session.commit()
    
    return jsonify({"message": "Mechanic deleted successfully"}), 200

@mechanic_bp.route("/login", methods=["POST"])
def login_mechanic():
    try:
        login_data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == login_data["email"])
    mechanic = db.session.execute(query).scalars().first()
    
    if not mechanic or mechanic.password != login_data["password"]:
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = encode_mechanic_token(mechanic.id)
    
    return jsonify({
        "message": "Mechanic login successful",
        "token": token
    }), 200
    
@mechanic_bp.route("/most-tickets", methods=["GET"])
def get_mechanics_by_ticket_count():
    query = (
        select(
            Mechanic.id,
            Mechanic.name,
            Mechanic.email,
            func.count(service_mechanics.c.service_id).label("ticket_count")
        )
        .join(service_mechanics, Mechanic.id == service_mechanics.c.mechanic_id)
        .group_by(Mechanic.id, Mechanic.name, Mechanic.email)
        .order_by(func.count(service_mechanics.c.service_id).desc())
    )

    results = db.session.execute(query).all()

    mechanics = [
        {
            "id": id,
            "name": name,
            "email": email,
            "ticket_count": ticket_count
        }
        for id, name, email, ticket_count in results
    ]

    return jsonify(mechanics), 200


        