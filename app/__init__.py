import os
from flask import Flask, request, session
from .models import db, AdminUser
from .admin import create_admin
from .routes.auth import auth_bp
from .routes.lang import lang_bp
from flask_babel import Babel
from .routes.api import api_bp
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import DevelopmentConfig, ProductionConfig

babel = Babel()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=None):
    app = Flask(__name__)

    # Выбор конфигурации
    if config_class is None:
        env = os.environ.get("FLASK_CONFIG", "development")
        if env == "production":
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig

    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # Подключение частей приложения
    create_admin(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(lang_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()  # ⚠️ в продакшене лучше убрать и использовать flask db upgrade

    babel.init_app(app, locale_selector=get_locale)
    return app


def get_locale():
    lang = (
        session.get("lang")
        or request.args.get("lang")
        or request.accept_languages.best_match(["en", "ru", "tk"])
    )
    print(f"Selected locale: {lang}")  # Для отладки
    return lang
