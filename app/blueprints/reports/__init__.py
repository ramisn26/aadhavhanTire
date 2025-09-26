from flask import Blueprint

bp = Blueprint('reports', __name__)

from app.blueprints.reports import routes