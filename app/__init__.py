from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
principal = Principal()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.billing import bp as billing_bp
    app.register_blueprint(billing_bp)

    from app.blueprints.inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from app.blueprints.reports import bp as reports_bp
    app.register_blueprint(reports_bp)

    return app