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
    extra_css = ["/static/css/admin.css"]
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
class MyAdminIndexView(AdminIndexView):
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
class ProductAdmin(SecureModelView):
   
    column_list = (
        "name_i18n", "slug", "brand_i18n", "category_i18n", "volume_or_weight",
    )
    column_labels = {
        "name_i18n": _l("Products"), 
        "brand_i18n": _l("Brands"),
        "category_i18n": _l("Categories"),
        "volume_or_weight": _l("Products"),
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "brand_i18n": lambda v, c, m, p: (_get_i18n_attr(m.brand, "name") if getattr(m, "brand", None) else ""),
        "category_i18n": lambda v, c, m, p: (_get_i18n_attr(m.category, "name") if getattr(m, "category", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "slug",
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
            relative_path="products/",
            url_relative_path="static/uploads/products/"
        ),
        "additional_images": MultiImageUploadField("Additional Images")
    }

    def on_model_change(self, form, model, is_created):
        if form.additional_images.data:
            model.additional_images = form.additional_images.data

# -----------------------------
# Brand Admin
# -----------------------------
class BrandAdmin(SecureModelView):
    column_list = ("name_i18n", "slug", "company_i18n")
    column_labels = {
        "name_i18n": _l("Brands"),
        "company_i18n": _l("Users"),
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "company_i18n": lambda v, c, m, p: (_get_i18n_attr(m.company, "name") if getattr(m, "company", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "subtitle_en", "subtitle_ru", "subtitle_tk",
        "slug",
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
            relative_path="brands/",
            url_relative_path="static/uploads/brands/"
        )
    }

# -----------------------------
# News Admin
# -----------------------------
class NewsAdmin(SecureModelView):
    column_list = ("title_i18n", "slug", "publication_date", "company_i18n")
    column_labels = {
        "title_i18n": _l("News"),
        "company_i18n": _l("Users"),
    }
    column_formatters = {
        "title_i18n": lambda v, c, m, p: _get_i18n_attr(m, "title"),
        "company_i18n": lambda v, c, m, p: (_get_i18n_attr(m.company, "name") if getattr(m, "company", None) else ""),
    }
    form_columns = [
        "title_en", "title_ru", "title_tk",
        "slug",
        "body_text_en", "body_text_ru", "body_text_tk",
        "publication_date", "image", "company", "products", "brands"
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
            relative_path="news/",
            url_relative_path="static/uploads/news/"
        )
    }

# -----------------------------
# Certificate Admin
# -----------------------------
class CertificateAdmin(SecureModelView):
    column_list = ("name_i18n", "company_i18n")
    column_labels = {
        "name_i18n": _l("Certificates") if False else _l("Products"),  
        "company_i18n": _l("Users"),
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "company_i18n": lambda v, c, m, p: (_get_i18n_attr(m.company, "name") if getattr(m, "company", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "description_en", "description_ru", "description_tk",
        "image", "company"
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
            "Certificate Image",
            base_path=os.path.join("app", "static", "uploads", "certificates"),
            relative_path="certificates/",
            url_relative_path="static/uploads/certificates/"
        )
    }

# -----------------------------
# Banner Admin
# -----------------------------
class BannerAdmin(SecureModelView):
    column_list = ("title_i18n", "link")
    column_labels = {
        "title_i18n": _l("News"),
    }
    column_formatters = {
        "title_i18n": lambda v, c, m, p: _get_i18n_attr(m, "title"),
    }
    form_columns = [
        "image", "link",
        "title_en", "title_ru", "title_tk",
        "description_en", "description_ru", "description_tk"
    ]
    form_overrides = {
        "title_en": TextAreaField,
        "title_ru": TextAreaField,
        "title_tk": TextAreaField,
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
    }
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"
    form_extra_fields = {
        "image": ImageUploadField(
            "Banner Image",
            base_path=os.path.join("app", "static", "uploads", "banners"),
            relative_path="banners/",
            url_relative_path="static/uploads/banners/"
        )
    }

# -----------------------------
# Company Admin
# -----------------------------
class CompanyAdmin(SecureModelView):
    column_list = ("name_i18n", "email", "phone")
    column_labels = {
        "name_i18n": _l("Users"),
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
class ProductCategoryAdmin(SecureModelView):
    column_list = ("name_i18n", "slug", "parent_i18n")
    column_labels = {
        "name_i18n": _l("Categories"),
        "parent_i18n": _l("Categories"),
    }
    column_formatters = {
        "name_i18n": lambda v, c, m, p: _get_i18n_attr(m, "name"),
        "parent_i18n": lambda v, c, m, p: (_get_i18n_attr(m.parent, "name") if getattr(m, "parent", None) else ""),
    }
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "slug",
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
            relative_path="categories/",
            url_relative_path="static/uploads/categories/"
        )
    }

# -----------------------------
# ContactMessage Admin
# -----------------------------
class ContactMessageAdmin(SecureModelView):
    form_columns = [
        "email", "message", "submission_date"
    ]
    form_overrides = {
        "message": TextAreaField,
    }
    edit_template = "admin/model/edit.html"
    create_template = "admin/model/create.html"

# -----------------------------
# Initialize Admin
# -----------------------------
def create_admin(app):
    admin = Admin(
        app,
        name=_l("Dashboard"),
        template_mode="bootstrap4",
        index_view=MyAdminIndexView()
    )

    admin.add_view(CompanyAdmin(Company, db.session, name=_l("Companies"), menu_icon_type="fa", menu_icon_value="fa fa-building"))
    admin.add_view(ProductAdmin(Product, db.session, name=_l("Products"), menu_icon_type="fa", menu_icon_value="fa fa-box"))
    admin.add_view(ProductCategoryAdmin(ProductCategory, db.session, name=_l("Categories"), menu_icon_type="fa", menu_icon_value="fa fa-list"))
    admin.add_view(BrandAdmin(Brand, db.session, name=_l("Brands"), menu_icon_type="fa", menu_icon_value="fa fa-tag"))
    admin.add_view(NewsAdmin(News, db.session, name=_l("News"), menu_icon_type="fa", menu_icon_value="fa fa-newspaper"))
    admin.add_view(CertificateAdmin(Certificate, db.session, name=_l("Certificates"), menu_icon_type="fa", menu_icon_value="fa fa-certificate"))
    admin.add_view(BannerAdmin(Banner, db.session, name=_l("Banners"), menu_icon_type="fa", menu_icon_value="fa fa-image"))
    admin.add_view(ContactMessageAdmin(ContactMessage, db.session, name=_l("Messages"), menu_icon_type="fa", menu_icon_value="fa fa-envelope"))
    admin.add_view(SecureModelView(NewsletterSubscriber, db.session, name=_l("Subscribers"), menu_icon_type="fa", menu_icon_value="fa fa-users"))
    admin.add_view(SecureModelView(AdminUser, db.session, name=_l("Users"), menu_icon_type="fa", menu_icon_value="fa fa-user-shield"))

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