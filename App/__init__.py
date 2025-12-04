from flask import Flask
from app.extensions import db
from app.blueprints.mechanic import mechanic_bp
from app.blueprints.service_ticket import service_ticket_bp
from app.extensions import db, migrate, ma, limiter, cache
from app.blueprints.parts import parts_bp   

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/tickets")

    # Cache Config
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60

    return app