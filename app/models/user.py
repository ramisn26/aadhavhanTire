from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_principal import Identity, UserNeed, RoleNeed
from app import db, login_manager
from app.models.base import BaseModel
from app.auth.rbac import ROLE_HIERARCHY

class Role(db.Model):
    """Role model for RBAC."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.Column(db.ARRAY(db.String), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.relationship('Role', back_populates='users')
    invoices_created = db.relationship('Invoice', back_populates='created_by')
    purchases_created = db.relationship('Purchase', back_populates='created_by')
    vendors = db.relationship('Vendor', back_populates='created_by')

    @property
    def password(self):
        """Password is not a readable attribute."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify password hash."""
        return check_password_hash(self.password_hash, password)
        
    def check_password(self, password):
        """Compatibility method for verify_password."""
        return self.verify_password(password)

    def has_permission(self, permission):
        """Check if user has a specific permission."""
        if not self.role:
            return False
        return permission in self.role.permissions

    def __repr__(self):
        """String representation of User."""
        return f'<User {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))