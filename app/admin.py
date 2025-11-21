import os
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask import redirect, url_for
from wtforms import FileField, TextAreaField
from flask_babel import gettext as _, lazy_gettext as _l, get_locale

from .models import (
    db, Product, ProductCategory, Brand, News, Banner,
    ContactMessage, NewsletterSubscriber, AdminUser,
    Company, Certificate
)

# -----------------------------
# Secure access for logged-in users
# -----------------------------
class SecureModelView(ModelView):
    # Подключаем общий CSS для всех страниц модели
    extra_css = ["/static/css/admin-new.css", "/static/css/admin.css"]
    # Глобальные скрипты (переключатель темы и быстрый поиск)
    extra_js = ["/static/js/admin-theme.js"]
    def is_accessible(self):
        from flask_login import current_user
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

# -----------------------------
# Admin Dashboard
# -----------------------------

# -----------------------------
# AutoSlugAdminMixin: hides slug from the form and ensures slug is generated if missing
# -----------------------------
class AutoSlugAdminMixin:
    # безопасно получаем form_excluded_columns, чтобы не было ошибки ObsoleteAttr
    _excluded = getattr(SecureModelView, "form_excluded_columns", [])
    if type(_excluded).__name__ == "ObsoleteAttr":
        _excluded = []

    # скрываем поле slug из формы
    form_excluded_columns = _excluded + ["slug"]

    def on_model_change(self, form, model, is_created):
        """
        Если slug пустой, генерируем его автоматически через модель.
        """
        try:
            if not getattr(model, "slug", None) and hasattr(model, "generate_slug_from_name"):
                model.generate_slug_from_name(session=db.session)
        except Exception:
            # логировать ошибку можно здесь
            pass
        return super().on_model_change(form, model, is_created)


class MyAdminIndexView(AdminIndexView):
    # Подключаем те же файлы стилей, что и у SecureModelView, чтобы дашборд и страницы списка совпадали
    extra_css = ["/static/css/admin-new.css", "/static/css/admin.css"]
    extra_js = ["/static/js/admin-theme.js"]

    @expose("/")
    def index(self):
        stats = {
            "companies": Company.query.count(),
            "products": Product.query.count(),
            "categories": ProductCategory.query.count(),
            "brands": Brand.query.count(),
            "news": News.query.count(),
            "certificates": Certificate.query.count(),
            "subscribers": NewsletterSubscriber.query.count(),
            "users": AdminUser.query.count(),
        }
        from flask_babel import get_locale
        return self.render("admin/dashboard.html", stats=stats, locale=get_locale())

    def is_visible(self):
        return True 
# -----------------------------
# Multi-image upload field
# -----------------------------
class MultiImageUploadField(FileField):
    def process_formdata(self, valuelist):
        self.data = []
        upload_folder = os.path.join("app", "static", "uploads", "products")
        os.makedirs(upload_folder, exist_ok=True)

        for f in valuelist:
            if f.filename:
                file_path = os.path.join(upload_folder, f.filename)
                f.save(file_path)
                self.data.append(os.path.join("static", "uploads", "products", f.filename))

    def _value(self):
        return self.data if self.data else []

# -----------------------------
# CKEditor custom template
# -----------------------------
EDIT_TEMPLATE = "admin/edit.html"
CREATE_TEMPLATE = "admin/create.html"

# -----------------------------
# Product Admin
# -----------------------------
class ProductAdmin(AutoSlugAdminMixin, SecureModelView):
   
    column_list = (
        "name_i18n", "slug", "brand_i18n", "category_i18n", "volume_or_weight",
    )
    column_labels = {
        "name_i18n": "Товары", 
        "name_en": "Название (EN)",
        "name_ru": "Название (RU)",
        "name_tk": "Название (TK)",
        "slug": "Адрес страницы",
        "description_en": "Описание (EN)",
        "description_ru": "Описание (RU)",
        "description_tk": "Описание (TK)",
        "volume_or_weight": "Объём/Вес",
        "image": "Основное изображение",
        "additional_images": "Дополнительные изображения",
        "packaging_details_en": "Детали упаковки (EN)",
        "packaging_details_ru": "Детали упаковки (RU)",
        "packaging_details_tk": "Детали упаковки (TK)",
        "brand_i18n": "Бренды",
        "category_i18n": "Категории",
        "brand": "Бренды",
        "category": "Категории",
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "brand_i18n": lambda v, c, m, p: (_get_i18n_attr(m.brand, "name") if getattr(m, "brand", None) else ""),
        "category_i18n": lambda v, c, m, p: (_get_i18n_attr(m.category, "name") if getattr(m, "category", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        
        "description_en", "description_ru", "description_tk",
        "volume_or_weight", "image", "additional_images",
        "packaging_details_en", "packaging_details_ru", "packaging_details_tk",
        "category", "brand"
    ]
    form_overrides = {
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
        "packaging_details_en": TextAreaField,
        "packaging_details_ru": TextAreaField,
        "packaging_details_tk": TextAreaField,
    }
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "image": ImageUploadField(
            "Main Image",
            base_path=os.path.join("app", "static", "uploads", "products"),
            relative_path="",
            url_relative_path="static/uploads/products/"
        ),
        "additional_images": MultiImageUploadField("Additional Images")
    }

    def on_model_change(self, form, model, is_created):
        if form.additional_images.data:
            model.additional_images = form.additional_images.data
        if form.image.data and hasattr(form.image.data, 'filename'):
            # Сохраняем полный путь к изображению
            model.image = f"static/uploads/products/{form.image.data.filename}"

# -----------------------------
# Brand Admin
# -----------------------------
class BrandAdmin(AutoSlugAdminMixin, SecureModelView):
    column_list = ("name_i18n", "slug", "company_i18n")
    column_labels = {
        "name_i18n": "Бренды",
        "name_en": "Название (EN)",
        "name_ru": "Название (RU)",
        "name_tk": "Название (TK)",
        "subtitle_en": "Подзаголовок (EN)",
        "subtitle_ru": "Подзаголовок (RU)",
        "subtitle_tk": "Подзаголовок (TK)",
        "slug": "Адрес страницы",
        "description_en": "Описание (EN)",
        "description_ru": "Описание (RU)",
        "description_tk": "Описание (TK)",
        "logo_image": "Логотип",
        "company_i18n": "Компания",
        "company": "Компания",
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "company_i18n": lambda v, c, m, p: (_get_i18n_attr(m.company, "name") if getattr(m, "company", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "subtitle_en", "subtitle_ru", "subtitle_tk",
        
        "description_en", "description_ru", "description_tk",
        "logo_image", "company"
    ]
    form_overrides = {
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
    }
    # Убираем rich editor для брендов - используем стандартные шаблоны
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "logo_image": ImageUploadField(
            "Logo",
            base_path=os.path.join("app", "static", "uploads", "brands"),
            relative_path="",
            url_relative_path="static/uploads/brands/"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.logo_image.data and hasattr(form.logo_image.data, 'filename'):
            # Сохраняем полный путь к изображению
            model.logo_image = f"static/uploads/brands/{form.logo_image.data.filename}"

# -----------------------------
# News Admin
# -----------------------------
class NewsAdmin(AutoSlugAdminMixin, SecureModelView):
    column_list = ("title_i18n", "slug", "publication_date", "company_i18n")
    column_labels = {
        "title_i18n": "Новости",
        "title_en": "Заголовок (EN)",
        "title_ru": "Заголовок (RU)",
        "title_tk": "Заголовок (TK)",
        "subtitle_en": "Подзаголовок (EN)",
        "subtitle_ru": "Подзаголовок (RU)",
        "subtitle_tk": "Подзаголовок (TK)",
        "slug": "Адрес страницы",
        "body_text_en": "Текст (EN)",
        "body_text_ru": "Текст (RU)",
        "body_text_tk": "Текст (TK)",
        "publication_date": "Дата публикации",
        "reading_minutes": "Время чтения (минут)",
        "image": "Изображение новости",
        "company_i18n": "Компания",
        "company": "Компания",
    }
    column_formatters = {
        "title_i18n": lambda v, c, m, p: _get_i18n_attr(m, "title"),
        "company_i18n": lambda v, c, m, p: (_get_i18n_attr(m.company, "name") if getattr(m, "company", None) else ""),
    }
    form_columns = [
        "title_en", "title_ru", "title_tk",
        "subtitle_en", "subtitle_ru", "subtitle_tk",
        
        "body_text_en", "body_text_ru", "body_text_tk",
        "publication_date", "reading_minutes", "image", "company"
    ]
    form_overrides = {
        "body_text_en": TextAreaField,
        "body_text_ru": TextAreaField,
        "body_text_tk": TextAreaField,
    }
    edit_template = EDIT_TEMPLATE
    create_template = CREATE_TEMPLATE
    form_extra_fields = {
        "image": ImageUploadField(
            "News Image",
            base_path=os.path.join("app", "static", "uploads", "news"),
            relative_path="",
            url_relative_path="static/uploads/news/"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.image.data and hasattr(form.image.data, 'filename'):
            # Сохраняем полный путь к изображению
            model.image = f"static/uploads/news/{form.image.data.filename}"

# -----------------------------
# Certificate Admin
# -----------------------------
class CertificateAdmin(AutoSlugAdminMixin, SecureModelView):
    column_list = ("id", "slug", "image")
    column_labels = {
        "id": "ID",
        "image": "Изображение сертификата",
        "slug": "Адрес страницы",
    }
    form_columns = [ "image"]
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "image": ImageUploadField(
            "Certificate Image",
            base_path=os.path.join("app", "static", "uploads", "certificates"),
            relative_path="",
            url_relative_path="static/uploads/certificates/"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.image.data and hasattr(form.image.data, 'filename'):
            model.image = f"static/uploads/certificates/{form.image.data.filename}"


# -----------------------------
# Banner Admin
# -----------------------------
class BannerAdmin(AutoSlugAdminMixin, SecureModelView):
    column_list = ("id", "slug", "image", "link")
    column_labels = {
        "id": "ID",
        "image": "Изображение баннера",
        "link": "Ссылка",
        "slug": "Адрес страницы",
    }
    form_columns = [ "image", "link"]
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "image": ImageUploadField(
            "Banner Image",
            base_path=os.path.join("app", "static", "uploads", "banners"),
            relative_path="",
            url_relative_path="static/uploads/banners/"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.image.data and hasattr(form.image.data, 'filename'):
            model.image = f"static/uploads/banners/{form.image.data.filename}"
# -----------------------------
# Company Admin
# -----------------------------
class CompanyAdmin(SecureModelView):
    column_list = ("name_i18n", "email", "phone")
    column_labels = {
        "name_i18n": "Компании",
        "name_en": "Название (EN)",
        "name_ru": "Название (RU)",
        "name_tk": "Название (TK)",
        "mission_en": "Миссия (EN)",
        "mission_ru": "Миссия (RU)",
        "mission_tk": "Миссия (TK)",
        "vision_en": "Видение (EN)",
        "vision_ru": "Видение (RU)",
        "vision_tk": "Видение (TK)",
        "phone": "Телефон",
        "email": "Email",
        "address_en": "Адрес (EN)",
        "address_ru": "Адрес (RU)",
        "address_tk": "Адрес (TK)",
        "map_coordinates": "Координаты на карте",
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "mission_en", "mission_ru", "mission_tk",
        "vision_en", "vision_ru", "vision_tk",
        "phone", "email",
        "address_en", "address_ru", "address_tk",
        "map_coordinates"
    ]
    form_overrides = {
        "mission_en": TextAreaField,
        "mission_ru": TextAreaField,
        "mission_tk": TextAreaField,
        "vision_en": TextAreaField,
        "vision_ru": TextAreaField,
        "vision_tk": TextAreaField,
        "address_en": TextAreaField,
        "address_ru": TextAreaField,
        "address_tk": TextAreaField,
    }
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"

# -----------------------------
# ProductCategory Admin
# -----------------------------
class ProductCategoryAdmin(AutoSlugAdminMixin, SecureModelView):
    column_list = ("name_i18n", "slug", "parent_i18n")
    column_labels = {
        "name_i18n": "Категории",
        "name_en": "Название (EN)",
        "name_ru": "Название (RU)",
        "name_tk": "Название (TK)",
        "slug": "Адрес страницы",
        "description_en": "Описание (EN)",
        "description_ru": "Описание (RU)",
        "description_tk": "Описание (TK)",
        "image": "Изображение категории",
        "parent_i18n": "Родительская категория",
        "parent": "Родительская категория",
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "parent_i18n": lambda v, c, m, p: (_get_i18n_attr(m.parent, "name") if getattr(m, "parent", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        
        "description_en", "description_ru", "description_tk",
        "image", "parent"
    ]
    form_overrides = {
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
    }
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "image": ImageUploadField(
            "Category Image",
            base_path=os.path.join("app", "static", "uploads", "categories"),
            relative_path="",
            url_relative_path="static/uploads/categories/"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.image.data and hasattr(form.image.data, 'filename'):
            # Сохраняем полный путь к изображению
            model.image = f"static/uploads/categories/{form.image.data.filename}"

# -----------------------------
# ContactMessage Admin
# -----------------------------
class ContactMessageAdmin(SecureModelView):
    column_list = ("name", "email", "submission_date")
    column_labels = {
        "name": "Имя",
        "email": "Email",
        "message": "Сообщение",
        "submission_date": "Дата отправки",
    }

# Enhanced view with labels for better UX
class NewsletterSubscriberAdmin(SecureModelView):
    column_list = ("email", "subscription_date")
    column_labels = {
        "email": "Email",
        "subscription_date": "Дата подписки",
    }
    form_columns = ["email", "subscription_date"]
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"

class AdminUserAdmin(SecureModelView):
    column_list = ("id", "username")
    column_labels = {
        "id": "ID",
        "username": "Имя пользователя",
        "password_hash": "Пароль",
    }
    form_columns = ["username", "password_hash"]
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"

# -----------------------------
# Initialize Admin
# -----------------------------
def create_admin(app):
    admin = Admin(
        app,
        name="Панель управления",
        template_mode="bootstrap4",
        index_view=MyAdminIndexView()
    )

    admin.add_view(CompanyAdmin(Company, db.session, name="Компании", menu_icon_type="fa", menu_icon_value="fa fa-building"))
    admin.add_view(ProductAdmin(Product, db.session, name="Товары", menu_icon_type="fa", menu_icon_value="fa fa-box"))
    admin.add_view(ProductCategoryAdmin(ProductCategory, db.session, name="Категории", menu_icon_type="fa", menu_icon_value="fa fa-list"))
    admin.add_view(BrandAdmin(Brand, db.session, name="Бренды", menu_icon_type="fa", menu_icon_value="fa fa-tag"))
    admin.add_view(NewsAdmin(News, db.session, name="Новости", menu_icon_type="fa", menu_icon_value="fa fa-newspaper"))
    admin.add_view(CertificateAdmin(Certificate, db.session, name="Сертификаты", menu_icon_type="fa", menu_icon_value="fa fa-certificate"))
    admin.add_view(BannerAdmin(Banner, db.session, name="Баннеры", menu_icon_type="fa", menu_icon_value="fa fa-image"))
    admin.add_view(ContactMessageAdmin(ContactMessage, db.session, name="Сообщения", menu_icon_type="fa", menu_icon_value="fa fa-envelope"))
    admin.add_view(NewsletterSubscriberAdmin(NewsletterSubscriber, db.session, name="Подписчики", menu_icon_type="fa", menu_icon_value="fa fa-users"))
    admin.add_view(AdminUserAdmin(AdminUser, db.session, name="Пользователи", menu_icon_type="fa", menu_icon_value="fa fa-user-shield"))

    return admin


# -----------------------------
# Helpers
# -----------------------------
def _current_lang_code():
    loc = str(get_locale() or "en")
    if loc.startswith("ru"):
        return "ru"
    if loc.startswith("tk"):
        return "tk"
    return "en"


def _get_i18n_attr(model_obj, base_name):
    if model_obj is None:
        return ""
    lang = _current_lang_code()
    preferred_attr = f"{base_name}_{lang}"
    value = getattr(model_obj, preferred_attr, None)
    if value:
        return value
    # fallback порядок: en -> ru -> tk
    for fallback in ("en", "ru", "tk"):
        val = getattr(model_obj, f"{base_name}_{fallback}", None)
        if val:
            return val
    return ""