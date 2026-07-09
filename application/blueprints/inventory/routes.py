from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from application.extensions import db
from application.models import Inventory

@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Inventory(**inventory_data)
    
    db.session.add(new_part)
    db.session.commit()
    
    return inventory_schema.jsonify(new_part), 201

@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    query = select(Inventory)
    inventory = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventory), 200

@inventory_bp.route("/<int:id>", methods=["GET"])
def get_inventory_item(id):
    query = select(Inventory).where(Inventory.id == id)
    part = db.session.execute(query).scalars().first()
    
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404
    
    return inventory_schema.jsonify(part), 200

@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_inventory(id):
    query = select(Inventory).where(Inventory.id == id)
    part = db.session.execute(query).scalars().first()
    
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404
    
    try: 
        inventory_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(part, key, value)
    
    db.session.commit()
    
    return inventory_schema.jsonify(part), 200

@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_inventory(id):
    query = select(Inventory).where(Inventory.id == id)
    part = db.session.execute(query).scalars().first()
    
    if not part:
        return jsonify({"error": "Inventory item not found"}), 404
    
    db.session.delete(part)
    db.session.commit()
    
    return jsonify({"message": "Inventory item deleted successfully"}), 200