from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, RoleNeed, UserNeed
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
principal = Principal()
migrate = Migrate()

# Import models before create_app
from app.models import *

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Set up Principal identity loading
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        if hasattr(identity, 'user'):
            identity.provides.add(UserNeed(identity.user.id))

            # Add the roles and permissions
            if identity.user.role:
                identity.provides.add(RoleNeed(identity.user.role.name))
                for permission in identity.user.role.permissions:
                    identity.provides.add(RoleNeed(permission))

    # Register blueprints with URL prefixes
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.billing import bp as billing_bp
    app.register_blueprint(billing_bp, url_prefix='/billing')

    from app.blueprints.inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    from app.blueprints.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')

    # Register main blueprint last (no prefix)
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Root URL handler
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('billing.quick_bill'))
        return redirect(url_for('auth.login'))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app