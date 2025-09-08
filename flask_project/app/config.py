import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

# Создадим папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
