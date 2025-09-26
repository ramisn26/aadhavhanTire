from flask_principal import Permission, RoleNeed, UserNeed

# Define base permissions
class RBACPermission(Permission):
    def __init__(self, permission_name):
        need = RoleNeed(permission_name)
        super(RBACPermission, self).__init__(need)

# User management permissions
admin_permission = RBACPermission('admin')
manage_users_permission = RBACPermission('manage_users')

# Inventory permissions
manage_inventory_permission = RBACPermission('manage_inventory')
view_inventory_permission = RBACPermission('view_inventory')

# Sales permissions
create_invoice_permission = RBACPermission('create_invoice')
view_invoice_permission = RBACPermission('view_invoice')
edit_invoice_permission = RBACPermission('edit_invoice')
void_invoice_permission = RBACPermission('void_invoice')

# Purchase permissions
create_purchase_permission = RBACPermission('create_purchase')
view_purchase_permission = RBACPermission('view_purchase')
edit_purchase_permission = RBACPermission('edit_purchase')
void_purchase_permission = RBACPermission('void_purchase')

# Report permissions
view_reports_permission = RBACPermission('view_reports')
export_reports_permission = RBACPermission('export_reports')

# Settings permissions
manage_settings_permission = RBACPermission('manage_settings')

# Define role hierarchy
ROLE_HIERARCHY = {
    'admin': {
        'permissions': [
            'admin',
            'manage_users',
            'manage_inventory',
            'view_inventory',
            'create_invoice',
            'view_invoice',
            'edit_invoice',
            'void_invoice',
            'create_purchase',
            'view_purchase',
            'edit_purchase',
            'void_purchase',
            'view_reports',
            'export_reports',
            'manage_settings'
        ]
    },
    'manager': {
        'permissions': [
            'manage_inventory',
            'view_inventory',
            'create_invoice',
            'view_invoice',
            'edit_invoice',
            'void_invoice',
            'create_purchase',
            'view_purchase',
            'edit_purchase',
            'void_purchase',
            'view_reports',
            'export_reports'
        ]
    },
    'sales': {
        'permissions': [
            'view_inventory',
            'create_invoice',
            'view_invoice',
            'edit_invoice',
            'view_reports'
        ]
    },
    'inventory': {
        'permissions': [
            'manage_inventory',
            'view_inventory',
            'create_purchase',
            'view_purchase',
            'edit_purchase',
            'view_reports'
        ]
    },
    'readonly': {
        'permissions': [
            'view_inventory',
            'view_invoice',
            'view_purchase',
            'view_reports'
        ]
    }
}