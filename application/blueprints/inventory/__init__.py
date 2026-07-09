from flask import Blueprint

inventory_bp = Blueprint("inventory_by", __name__)

from . import routes