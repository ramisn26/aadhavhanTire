from functools import wraps
from flask import current_app
from flask_login import current_user
from flask_principal import Permission, RoleNeed

def permission_required(permission):
    """Decorator to check if the user has the required permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            
            if not current_user.has_permission(permission):
                return current_app.login_manager.unauthorized()
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(role):
    """Decorator to check if the user has the required role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            
            if not current_user.has_role(role):
                return current_app.login_manager.unauthorized()
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to check if the user is an admin."""
    return role_required('admin')(f)