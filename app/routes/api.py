from flask import Blueprint, request, jsonify
from ..models import db, Company, Certificate, Brand, ProductCategory, Product, News, ContactMessage, NewsletterSubscriber, Banner

api_bp = Blueprint("api", __name__)

def success_response(data=None, message="Success"):
    """Создает успешный JSON ответ"""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response)

def error_response(message="Error", status_code=400):
    """Создает ошибочный JSON ответ"""
    return jsonify({"success": False, "message": message}), status_code

def get_or_404(model, object_id):
    obj = model.query.get(object_id)
    if not obj:
        return error_response(f"{model.__name__} with id {object_id} not found", 404)
    return obj


def _absolute_url(path: str):
    if not path:
        return None
    
    # Если уже абсолютный URL, возвращаем как есть
    if isinstance(path, str) and (path.startswith("http://") or path.startswith("https://")):
        return path
    
    # Получаем базовый URL из запроса
    prefix = request.host_url.rstrip("/")
    
    # Нормализуем путь к статическому файлу
    if path.startswith("static/"):
        # Путь уже содержит static/, добавляем только /
        normalized = f"/{path}"
    elif path.startswith("/static/"):
        # Путь уже содержит /static/, используем как есть
        normalized = path
    else:
        # Добавляем /static/ к началу пути
        if path.startswith("/"):
            normalized = f"/static{path}"
        else:
            normalized = f"/static/{path}"
    
    return f"{prefix}{normalized}"
    
@api_bp.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    data = [c.to_dict() for c in companies]
    return success_response(data, "Companies retrieved successfully")

@api_bp.route("/companies/<int:company_id>", methods=["GET"])
def get_company(company_id):
    c = get_or_404(Company, company_id)
    if isinstance(c, tuple):
        return c
    return jsonify(c.to_dict())

# ---------- CERTIFICATE ----------
@api_bp.route("/certificates", methods=["GET"])
def get_certificates():
    items = Certificate.query.all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Certificates retrieved successfully")

@api_bp.route("/certificates/<int:item_id>", methods=["GET"])
def get_certificate(item_id):
    i = get_or_404(Certificate, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Certificate retrieved successfully")
@api_bp.route("/certificates/<string:slug>", methods=["GET"])
def get_certificate_by_slug(slug):
    i = Certificate.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Certificate with slug {slug} not found", 404)
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Certificate retrieved successfully")

# ---------- BRAND ----------
@api_bp.route("/brands", methods=["GET"])
def get_brands():
    items = Brand.query.all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Brands retrieved successfully")

@api_bp.route("/brands/<int:item_id>", methods=["GET"])
def get_brand(item_id):
    i = get_or_404(Brand, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Brand retrieved successfully")

# ---------- BRAND by SLUG ----------
@api_bp.route("/brands/<string:slug>", methods=["GET"])
def get_brand_by_slug(slug):
    i = Brand.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Brand with slug {slug} not found", 404)
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Brand retrieved successfully")

# ---------- CATEGORY ----------
@api_bp.route("/categories", methods=["GET"])
def get_categories():
    items = ProductCategory.query.all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Categories retrieved successfully")
@api_bp.route("/categories/parents", methods=["GET"])
def get_parent_categories():
    items = ProductCategory.query.filter_by(parent_category_id=None).all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Parent categories retrieved successfully")

@api_bp.route("/categories/<int:item_id>", methods=["GET"])
def get_category(item_id):
    i = get_or_404(ProductCategory, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Category retrieved successfully")

# ---------- PRODUCT ----------
@api_bp.route("/products", methods=["GET"])
def get_products():
    category_id = request.args.get("category_id", type=int)
    category_slug = request.args.get("category", type=str)
    search_query= request.args.get("q", type=str)
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=20, type=int)
    query = Product.query

    if category_id:
        # Фильтрация по id категории и её дочерним
        child_categories = ProductCategory.query.filter_by(parent_category_id=category_id).all()
        child_ids = [cat.id for cat in child_categories]
        all_category_ids = [category_id] + child_ids
        query = query.filter(Product.category_id.in_(all_category_ids))
    elif category_slug:
        # Фильтрация по слагу категории и её дочерним
        parent_category = ProductCategory.query.filter_by(slug=category_slug).first()
        if parent_category:
            child_categories = ProductCategory.query.filter_by(parent_category_id=parent_category.id).all()
            child_ids = [cat.id for cat in child_categories]
            all_category_ids = [parent_category.id] + child_ids
            query = query.filter(Product.category_id.in_(all_category_ids))
        else:
            # Если категория не найдена — вернуть пустой список с мета
            return success_response({
                "products": [],
                "meta": {
                    "total": 0,
                    "current_page": page,
                    "last_page": 1
                }
            })
# фильтрация по поисковому запросу
    if search_query:
        query = query.filter(
            (Product.name_en.ilike(f"%{search_query}%")) |
            (Product.name_ru.ilike(f"%{search_query}%")) |
            (Product.name_tk.ilike(f"%{search_query}%")) |
            (Product.description_en.ilike(f"%{search_query}%")) |
            (Product.description_ru.ilike(f"%{search_query}%")) |
            (Product.description_tk.ilike(f"%{search_query}%"))
        )

    total = query.count()
    last_page = max((total + limit - 1) // limit, 1)
    products = query.offset((page - 1) * limit).limit(limit).all()

    data = {
        "products": [product.to_dict() for product in products],
        "meta": {
            "total": total,
            "current_page": page,
            "last_page": last_page
        }
    }
    return success_response(data, "Products retrieved successfully")

@api_bp.route("/products/<int:item_id>", methods=["GET"])
def get_product(item_id):
    i = get_or_404(Product, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Product retrieved successfully")
from sqlalchemy.sql.expression import func

@api_bp.route("/products/recommendations/<int:exclude_id>", methods=["GET"])
def get_random_products(exclude_id):
    items = Product.query.filter(Product.id != exclude_id).order_by(func.random()).limit(3).all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Random products retrieved successfully")

# ---------- PRODUCT by SLUG ----------
@api_bp.route("/products/<string:slug>", methods=["GET"])
def get_product_by_slug(slug):
    i = Product.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Product with slug {slug} not found", 404)
    data = i.to_dict(absolute_url_func=_absolute_url)
    # category и brand можно добавить отдельно, если нужно
    return success_response(data, "Product retrieved successfully")

# ---------- NEWS ----------
@api_bp.route("/news", methods=["GET"])
def get_news():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return error_response("Invalid page or limit", 400)

    query = News.query.order_by(News.publication_date.desc())  # можно сортировать по дате публикации

    total = query.count()
    last_page = max((total + limit - 1) // limit, 1)
    items = query.offset((page - 1) * limit).limit(limit).all()

    news_items = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    data = {
        "news": news_items,
        "meta": {
            "total": total,
            "current_page": page,
            "last_page": last_page
        }
    }
    return success_response(data, "News retrieved successfully")

@api_bp.route("/news/<int:item_id>", methods=["GET"])
def get_news_item(item_id):
    i = get_or_404(News, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "News item retrieved successfully")
@api_bp.route("/news/recommendations/<int:exclude_id>", methods=["GET"])
def get_random_news(exclude_id):
    items = News.query.filter(News.id != exclude_id).order_by(func.random()).limit(3).all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Random news retrieved successfully")

# ---------- NEWS by SLUG ----------
@api_bp.route("/news/<string:slug>", methods=["GET"])
def get_news_by_slug(slug):
    i = News.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"News with slug {slug} not found", 404)
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "News item retrieved successfully")

# ---------- BANNER ----------
@api_bp.route("/banners", methods=["GET"])
def get_banners():
    items = Banner.query.all()
    data = [i.to_dict(absolute_url_func=_absolute_url) for i in items]
    return success_response(data, "Banners retrieved successfully")

@api_bp.route("/banners/<int:item_id>", methods=["GET"])
def get_banner(item_id):
    i = get_or_404(Banner, item_id)
    if isinstance(i, tuple):
        return i
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Banner retrieved successfully")
@api_bp.route("/banners/<string:slug>", methods=["GET"])
def get_banner_by_slug(slug):
    i = Banner.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Banner with slug {slug} not found", 404)
    data = i.to_dict(absolute_url_func=_absolute_url)
    return success_response(data, "Banner retrieved successfully")

# ---------- CONTACT MESSAGE (only POST) ----------
@api_bp.route("/contact_messages", methods=["POST"])
def create_contact_message():
    try:
        data = request.json
        if not data or 'message' not in data or 'email' not in data:
            return error_response("Email and message fields are required", 400)

    
        name_value = (data.get('name') or data.get('full_name') or '').strip()

        msg = ContactMessage(
            name=name_value or None,
            email=data['email'],
            message=data['message']
        )
        db.session.add(msg)
        db.session.commit()
        return success_response({"id": msg.id}, "Contact message created successfully"), 201
    except Exception as e:
        return error_response(f"Error creating contact message: {str(e)}", 500)

# ---------- NEWSLETTER SUBSCRIBER (only POST) ----------
@api_bp.route("/newsletter_subscribers", methods=["POST"])
def create_newsletter_subscriber():
    try:
        data = request.json
        if not data or 'email' not in data:
            return error_response("Email field is required", 400)
        email = (data.get('email') or '').strip().lower()
        if not email:
            return error_response("Email field is required", 400)

        # Idempotent create: if exists, return 200 with existing id
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if existing:
            return success_response({"id": existing.id}, "Already subscribed"), 200

        sub = NewsletterSubscriber(email=email)
        db.session.add(sub)
        db.session.commit()
        return success_response({"id": sub.id}, "Newsletter subscriber created successfully"), 201
    except Exception as e:
        return error_response(f"Error creating newsletter subscriber: {str(e)}", 500)
