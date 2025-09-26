from flask import Blueprint, render_template
from flask_login import login_required
from app.auth.decorators import admin_required, permission_required
from app.auth.rbac import (
    manage_users_permission,
    manage_inventory_permission,
    create_invoice_permission,
    create_purchase_permission,
    view_reports_permission
)

bp = Blueprint('admin', __name__)

@bp.route('/admin')
@admin_required
def admin_panel():
    """Admin panel - requires admin role."""
    return render_template('admin/index.html')

@bp.route('/users')
@permission_required('manage_users')
def manage_users():
    """User management - requires manage_users permission."""
    return render_template('admin/users.html')

@bp.route('/inventory/manage')
@permission_required('manage_inventory')
def manage_inventory():
    """Inventory management - requires manage_inventory permission."""
    return render_template('admin/inventory.html')

@bp.route('/reports')
@permission_required('view_reports')
def view_reports():
    """View reports - requires view_reports permission."""
    return render_template('admin/reports.html')