from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from config import DevelopmentConfig
from .extensions import db, ma, limiter, cache
from .models import Customer, Service, Mechanic, Inventory
from .blueprints.customer import customer_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp
from .blueprints.inventory import inventory_bp

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix= "/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Mechanic Shop API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    with app.app_context():
        db.create_all()
        
    return app