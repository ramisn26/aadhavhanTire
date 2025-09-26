from flask import Blueprint

bp = Blueprint('inventory', __name__)

from app.blueprints.inventory import routes