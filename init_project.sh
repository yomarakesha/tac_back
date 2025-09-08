#!/bin/bash

PROJECT_NAME="flask_project"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# основные файлы
touch config.py requirements.txt run.py

# папка приложения
mkdir -p app/{routes,templates,static/{css,js,images}}
touch app/__init__.py app/models.py app/admin.py app/forms.py
touch app/routes/__init__.py app/routes/auth.py

# run.py
cat > run.py <<EOL
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
EOL

# __init__.py
cat > app/__init__.py <<EOL
from flask import Flask
from .models import db
from .admin import create_admin, login_manager
from .routes.auth import auth_bp


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
EOL

# base.html
cat > app/templates/base.html <<EOL
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мой сайт{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
EOL

# login.html
cat > app/templates/login.html <<EOL
{% extends "base.html" %}
{% block title %}Вход в админку{% endblock %}
{% block content %}
<div class="login-box">
    <h2>Вход</h2>
    <form method="post">
        <label>Логин</label>
        <input type="text" name="username" required>
        <label>Пароль</label>
        <input type="password" name="password" required>
        <button type="submit">Войти</button>
    </form>
</div>
{% endblock %}
EOL

# style.css
cat > app/static/css/style.css <<EOL
body {
    font-family: Arial, sans-serif;
    background: #f9f9f9;
}
.login-box {
    width: 300px;
    margin: 100px auto;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
.login-box input {
    width: 100%;
    padding: 8px;
    margin: 8px 0;
}
.login-box button {
    width: 100%;
    padding: 10px;
}
EOL

# requirements
cat > requirements.txt <<EOL
flask
flask_sqlalchemy
flask_admin
flask_login
werkzeug
EOL

echo "✅ Проект '$PROJECT_NAME' создан и готов к запуску: python run.py"
