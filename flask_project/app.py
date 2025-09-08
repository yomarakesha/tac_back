from flask import Flask
from app.models import db
from app.admin import create_admin, login_manager
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    create_admin(app)

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app



