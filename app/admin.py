import os
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from flask import redirect, url_for
from wtforms import FileField, TextAreaField
from flask_babel import gettext as _

from .models import (
    db, Product, ProductCategory, Brand, News, Banner,
    ContactMessage, NewsletterSubscriber, AdminUser,
    Company, Certificate
)

# -----------------------------
# Secure access for logged-in users
# -----------------------------
class SecureModelView(ModelView):
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
        return False  # скрываем из бокового меню

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

# -----------------------------
# Product Admin
# -----------------------------
class ProductAdmin(SecureModelView):
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
    form_template = EDIT_TEMPLATE
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
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "slug",
        "description_en", "description_ru", "description_tk",
        "logo_image", "company"
    ]
    form_overrides = {
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
    }
    form_template = EDIT_TEMPLATE
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
    form_template = EDIT_TEMPLATE
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
    form_template = EDIT_TEMPLATE
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
    form_template = EDIT_TEMPLATE
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
    form_template = EDIT_TEMPLATE

# -----------------------------
# ProductCategory Admin
# -----------------------------
class ProductCategoryAdmin(SecureModelView):
    form_columns = [
        "name_en", "name_ru", "name_tk",
        "slug",
        "description_en", "description_ru", "description_tk",
        "parent"
    ]
    form_overrides = {
        "description_en": TextAreaField,
        "description_ru": TextAreaField,
        "description_tk": TextAreaField,
    }
    form_template = EDIT_TEMPLATE

# -----------------------------
# ContactMessage Admin
# -----------------------------
class ContactMessageAdmin(SecureModelView):
    form_columns = [
        "full_name", "email",
        "message_en", "message_ru", "message_tk",
        "submission_date"
    ]
    form_overrides = {
        "message_en": TextAreaField,
        "message_ru": TextAreaField,
        "message_tk": TextAreaField,
    }

# -----------------------------
# Initialize Admin
# -----------------------------
def create_admin(app):
    admin = Admin(
        app,
        name="Admin Panel",
        template_mode="bootstrap4",  # Изменено на bootstrap4 для совместимости
        index_view=MyAdminIndexView()
    )

    admin.add_view(CompanyAdmin(Company, db.session, name="Companies"))
    admin.add_view(ProductAdmin(Product, db.session, name="Products"))
    admin.add_view(ProductCategoryAdmin(ProductCategory, db.session, name="Categories"))
    admin.add_view(BrandAdmin(Brand, db.session, name="Brands"))
    admin.add_view(NewsAdmin(News, db.session, name="News"))
    admin.add_view(CertificateAdmin(Certificate, db.session, name="Certificates"))
    admin.add_view(BannerAdmin(Banner, db.session, name="Banners"))
    admin.add_view(ContactMessageAdmin(ContactMessage, db.session, name="Messages"))
    admin.add_view(SecureModelView(NewsletterSubscriber, db.session, name="Subscribers"))
    admin.add_view(SecureModelView(AdminUser, db.session, name="Users"))

    return admin