from flask import Flask, request, session
from .models import db, AdminUser
from .admin import create_admin
from .routes.auth import auth_bp
from .routes.lang import lang_bp
from flask_babel import Babel
from .routes.api import api_bp
from flask_login import LoginManager
from flask_migrate import Migrate

babel = Babel()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Отключение кэша шаблонов для разработки

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # user_loader для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    create_admin(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(lang_bp)  # ✅ регистрация blueprint для смены языка
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    babel.init_app(app, locale_selector=get_locale)
    return app

# Функция выбора локали
def get_locale():
    lang = (
        session.get('lang')
        or request.args.get('lang')
        or request.accept_languages.best_match(['en', 'ru', 'tk'])
    )
    print(f"Selected locale: {lang}")  # Для отладки
    return lang