"""Routes for reports and analytics."""
from flask import render_template
from flask_login import login_required
from app.blueprints.reports import bp

@bp.route('/', methods=['GET'])
@login_required
def index():
    """Reports dashboard."""
    return render_template('reports/index.html')