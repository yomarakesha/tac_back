import os

# Папка instance — Flask сам знает, где она
# (по умолчанию: <корень проекта>/instance)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), "instance")
os.makedirs(INSTANCE_PATH, exist_ok=True)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-placeholder")

    # 📦 База по умолчанию в instance/database.db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_PATH, 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BABEL_TRANSLATION_DIRECTORIES = "translations"
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # Папка для загрузок
    UPLOAD_FOLDER = UPLOAD_FOLDER


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
