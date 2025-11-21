from flask import Flask
from .extensions import db, ma, migrate

def create_app():

    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp

    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    return app