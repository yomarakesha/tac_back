# app/routes/lang.py
from flask import Blueprint, redirect, request, session, url_for

lang_bp = Blueprint("lang", __name__)

@lang_bp.route("/set_lang/<lang>")
def set_lang(lang):
    # Проверяем, что язык поддерживается
    if lang in ["en", "ru", "tk"]:
        session["lang"] = lang
        print(f"Set session['lang'] to {lang}")  # Для отладки
    next_url = request.referrer or url_for("admin.index")
    return redirect(next_url)