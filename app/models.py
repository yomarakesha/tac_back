from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Админ-пользователь
class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Основная модель компании
class Company(db.Model):
    def to_dict(self):
        return {
            "id": self.id,
            "name_en": self.name_en,
            "name_ru": self.name_ru,
            "name_tk": self.name_tk,
            "mission_en": self.mission_en,
            "mission_ru": self.mission_ru,
            "mission_tk": self.mission_tk,
            "vision_en": self.vision_en,
            "vision_ru": self.vision_ru,
            "vision_tk": self.vision_tk,
            "phone": self.phone,
            "email": self.email,
            "address_en": self.address_en,
            "address_ru": self.address_ru,
            "address_tk": self.address_tk,
            "map_coordinates": self.map_coordinates
        }
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(250), nullable=True)
    name_ru = db.Column(db.String(250), nullable=True)
    name_tk = db.Column(db.String(250), nullable=True)
    mission_en = db.Column(db.Text)
    mission_ru = db.Column(db.Text)
    mission_tk = db.Column(db.Text)
    vision_en = db.Column(db.Text)
    vision_ru = db.Column(db.Text)
    vision_tk = db.Column(db.Text)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    address_en = db.Column(db.Text)
    address_ru = db.Column(db.Text)
    address_tk = db.Column(db.Text)
    map_coordinates = db.Column(db.String(100))

# Сертификаты
class Certificate(db.Model):
    def to_dict(self, absolute_url_func=None):
        image_url = absolute_url_func(self.image) if absolute_url_func else self.image
        return {
            "id": self.id,
            "image": image_url,
            "slug": getattr(self, "slug", None)
        }
    __tablename__ = "certificate"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(250))
    slug = db.Column(db.String(120), unique=True, nullable=False)

# Торговые марки
class Brand(db.Model):
    def to_dict(self, absolute_url_func=None):
        logo_url = absolute_url_func(self.logo_image) if absolute_url_func else self.logo_image
        return {
            "id": self.id,
            "name_en": self.name_en,
            "name_ru": self.name_ru,
            "name_tk": self.name_tk,
            "subtitle_en": self.subtitle_en,
            "subtitle_ru": self.subtitle_ru,
            "subtitle_tk": self.subtitle_tk,
            "slug": self.slug,
            "description_en": self.description_en,
            "description_ru": self.description_ru,
            "description_tk": self.description_tk,
            "company_id": self.company_id,
            "logo_image": logo_url
        }
    __tablename__ = "brand"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_ru = db.Column(db.String(120), nullable=False)
    name_tk = db.Column(db.String(120), nullable=False)
    subtitle_en = db.Column(db.String(250))
    subtitle_ru = db.Column(db.String(250))
    subtitle_tk = db.Column(db.String(250))
    logo_image = db.Column(db.String(250))
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='brands')

# Категории товаров
class ProductCategory(db.Model):
    def to_dict(self, absolute_url_func=None):
        image_url = absolute_url_func(self.image) if absolute_url_func else self.image
        return {
            "id": self.id,
            "name_en": self.name_en,
            "name_ru": self.name_ru,
            "name_tk": self.name_tk,
            "slug": self.slug,
            "description_en": self.description_en,
            "description_ru": self.description_ru,
            "description_tk": self.description_tk,
            "image": image_url,
            "parent_category_id": self.parent_category_id
        }
    __tablename__ = "product_category"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_ru = db.Column(db.String(120), nullable=False)
    name_tk = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    image = db.Column(db.String(250))
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=True)
    parent = db.relationship('ProductCategory', remote_side=[id], backref='subcategories')

# Товары
class Product(db.Model):
    def to_dict(self, absolute_url_func=None):
        image_url = absolute_url_func(self.image) if absolute_url_func else self.image
        additional_images = [absolute_url_func(p) for p in (self.additional_images or [])] if absolute_url_func else (self.additional_images or [])
        return {
            "id": self.id,
            "name_en": self.name_en,
            "name_ru": self.name_ru,
            "name_tk": self.name_tk,
            "slug": self.slug,
            "description_en": self.description_en,
            "description_ru": self.description_ru,
            "description_tk": self.description_tk,
            "volume_or_weight": self.volume_or_weight,
            "image": image_url,
            "additional_images": additional_images,
            "packaging_details_en": self.packaging_details_en,
            "packaging_details_ru": self.packaging_details_ru,
            "packaging_details_tk": self.packaging_details_tk,
            "category_id": self.category_id,
            "brand_id": self.brand_id
        }
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(250), nullable=False)
    name_ru = db.Column(db.String(250), nullable=False)
    name_tk = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    volume_or_weight = db.Column(db.String(50))
    image = db.Column(db.String(250))
    additional_images = db.Column(db.JSON, default=[])
    packaging_details_en = db.Column(db.Text)
    packaging_details_ru = db.Column(db.Text)
    packaging_details_tk = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    category = db.relationship('ProductCategory', backref='products')
    brand = db.relationship('Brand', backref='products')

# Новости
class News(db.Model):
    def to_dict(self, absolute_url_func=None):
        image_url = absolute_url_func(self.image) if absolute_url_func else self.image
        return {
            "id": self.id,
            "title_en": self.title_en,
            "title_ru": self.title_ru,
            "title_tk": self.title_tk,
            "subtitle_en": self.subtitle_en,
            "subtitle_ru": self.subtitle_ru,
            "subtitle_tk": self.subtitle_tk,
            "slug": self.slug,
            "publication_date": self.publication_date,
            "image": image_url,
            "body_text_en": self.body_text_en,
            "body_text_ru": self.body_text_ru,
            "body_text_tk": self.body_text_tk,
            "reading_minutes": self.reading_minutes,
            "company_id": self.company_id
        }
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(250), nullable=False)
    title_ru = db.Column(db.String(250), nullable=False)
    title_tk = db.Column(db.String(250), nullable=False)
    subtitle_en = db.Column(db.String(250))
    subtitle_ru = db.Column(db.String(250))
    subtitle_tk = db.Column(db.String(250))
    slug = db.Column(db.String(250), unique=True, nullable=False)
    publication_date = db.Column(db.Date, default=datetime.utcnow().date)
    image = db.Column(db.String(250))
    body_text_en = db.Column(db.Text)
    body_text_ru = db.Column(db.Text)
    body_text_tk = db.Column(db.Text)
    reading_minutes = db.Column(db.Integer, default=5)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='news')

# Сообщения из контактной формы
class ContactMessage(db.Model):
    __tablename__ = "contact_message"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

# Подписчики рассылки
class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscriber"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)

# Баннеры
class Banner(db.Model):
    def to_dict(self, absolute_url_func=None):
        image_url = absolute_url_func(self.image) if absolute_url_func else self.image
        return {
            "id": self.id,
            "image": image_url,
            "link": self.link,
            "slug": getattr(self, "slug", None)
        }
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(250))
    link = db.Column(db.String(250))
    slug = db.Column(db.String(120), unique=True, nullable=False)
