from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select

from . import customer_bp
from .customerSchemas import customer_schema, customers_schema, login_schema
from application.extensions import db, cache, limiter
from application.models import Customer, Service
from application.utils import encode_token, token_required

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
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    
    query = select(Customer)
    customers = db.paginate(
        query,
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        "customers": customers_schema.dump(customers.items),
        "page": customers.page,
        "per_page": customers.per_page,
        "total": customers.total,
        "pages": customers.pages
    }), 200


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
@token_required
def update_customer(logged_in_customer_id, customer_id):
    if logged_in_customer_id != customer_id:
        return jsonify({"error": "Unauthorized"}), 403
    
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
@token_required
def delete_customer(logged_in_customer_id, customer_id):
    if logged_in_customer_id != customer_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    # Delete related service tickets first so customer_id never gets set to NULL
    for ticket in customer.service_tickets:
        ticket.mechanics.clear()
        ticket.parts.clear()
        db.session.delete(ticket)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200

@customer_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login_customer():
    try:
        login_data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == login_data["email"])
    customer = db.session.execute(query).scalars().first()
    
    if not customer or customer.password != login_data["password"]:
        return jsonify({"error": "Invalid email or password"}), 401
    
    token = encode_token(customer.id)
    
    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200
    
@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    query = select(Service).where(Service.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    from application.blueprints.service_ticket.schemas import service_tickets_schema
    
    return service_tickets_schema.jsonify(tickets), 200
        