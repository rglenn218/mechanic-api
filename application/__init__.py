from flask import Flask
from config import Config
from .extensions import db, ma, limiter, cache
from .models import Customer, Service, Mechanic, Inventory
from .blueprints.customer import customer_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp
from .blueprints.inventory import inventory_bp

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix= "/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    
    with app.app_context():
        db.create_all()
        
    return app