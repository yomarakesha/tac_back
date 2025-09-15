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
    __tablename__ = "certificate"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(250), nullable=False)
    name_ru = db.Column(db.String(250), nullable=False)
    name_tk = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250))
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='certificates')

# Торговые марки
class Brand(db.Model):
    __tablename__ = "brand"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_ru = db.Column(db.String(120), nullable=False)
    name_tk = db.Column(db.String(120), nullable=False)
    logo_image = db.Column(db.String(250))
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='brands')

# Категории товаров
class ProductCategory(db.Model):
    __tablename__ = "product_category"
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_ru = db.Column(db.String(120), nullable=False)
    name_tk = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    description_tk = db.Column(db.Text)
    image = db.Column(db.String(250))  # изображение категории
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=True)
    parent = db.relationship('ProductCategory', remote_side=[id], backref='subcategories')

# Товары
class Product(db.Model):
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
    image = db.Column(db.String(250))  # главное изображение
    additional_images = db.Column(db.JSON, default=[])  # список картинок
    packaging_details_en = db.Column(db.Text)
    packaging_details_ru = db.Column(db.Text)
    packaging_details_tk = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    category = db.relationship('ProductCategory', backref='products')
    brand = db.relationship('Brand', backref='products')

# Промежуточная таблица для many-to-many связи News-Product
news_product_association = db.Table('news_product',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

# Промежуточная таблица для many-to-many связи News-Brand
news_brand_association = db.Table('news_brand',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True),
    db.Column('brand_id', db.Integer, db.ForeignKey('brand.id'), primary_key=True)
)

# Новости
class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(250), nullable=False)
    title_ru = db.Column(db.String(250), nullable=False)
    title_tk = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    publication_date = db.Column(db.Date, default=datetime.utcnow().date)
    image = db.Column(db.String(250))
    body_text_en = db.Column(db.Text)
    body_text_ru = db.Column(db.Text)
    body_text_tk = db.Column(db.Text)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='news')
    products = db.relationship('Product', secondary=news_product_association, backref='related_news')
    brands = db.relationship('Brand', secondary=news_brand_association, backref='related_news')

# Сообщения из контактной формы
class ContactMessage(db.Model):
    __tablename__ = "contact_message"
    id = db.Column(db.Integer, primary_key=True)
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
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(250))
    link = db.Column(db.String(250))
    title_en = db.Column(db.String(250))
    title_ru = db.Column(db.String(250))
    title_tk = db.Column(db.String(250))
    description_en = db.Column(db.String(500))
    description_ru = db.Column(db.String(500))
    description_tk = db.Column(db.String(500))
