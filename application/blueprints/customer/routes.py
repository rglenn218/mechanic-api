from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from . import customer_bp
from .customerSchemas import customer_schema, customers_schema
from application.extensions import db
from application.models import Customer

# CREATE customer
@customer_bp.route("/", methods=["POST"])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data["email"])
    existing_customer = db.session.execute(query).scalars().first()

    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(**customer_data)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


# READ all customers
@customer_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers), 200


# READ one customer
@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


# UPDATE customer
@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if "email" in customer_data:
        query = select(Customer).where(Customer.email == customer_data["email"])
        existing_customer = db.session.execute(query).scalars().first()

        if existing_customer and existing_customer.id != customer.id:
            return jsonify({"error": "Email already associated with an account."}), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()

    return customer_schema.jsonify(customer), 200


# DELETE customer
@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200