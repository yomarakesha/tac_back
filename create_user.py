from app import create_app
from app.models import db, AdminUser

app = create_app()

with app.app_context():
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    if AdminUser.query.filter_by(username=username).first():
        print(f"❌ Пользователь {username} уже существует!")
    else:
        user = AdminUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Пользователь {username} успешно создан!")
