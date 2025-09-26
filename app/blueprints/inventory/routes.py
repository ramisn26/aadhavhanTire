"""Routes for inventory management."""
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.inventory import Item, Service
from app.models.vendor import Vendor
from app import db
from app.blueprints.inventory import bp

@bp.route('/purchase-entry', methods=['GET', 'POST'])
@login_required
def purchase_entry():
    """Purchase entry form."""
    return render_template('inventory/purchase_entry.html')

@bp.route('/items', methods=['GET'])
@login_required
def items_list():
    """List all items."""
    items = Item.query.all()
    return render_template('inventory/items_list.html', items=items)

@bp.route('/services', methods=['GET'])
@login_required
def services_list():
    """List all services."""
    services = Service.query.all()
    return render_template('inventory/services_list.html', services=services)

@bp.route('/vendors', methods=['GET'])
@login_required
def vendors_list():
    """List all vendors."""
    vendors = Vendor.query.all()
    return render_template('inventory/vendors_list.html', vendors=vendors)