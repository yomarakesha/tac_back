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
    if isinstance(path, str) and (path.startswith("http://") or path.startswith("https://")):
        return path
    prefix = request.host_url.rstrip("/")
    normalized = path if path.startswith("/") else f"/{path}"
    return f"{prefix}{normalized}"
    
@api_bp.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    data = [
        {
            "id": c.id,
            "name_en": c.name_en,
            "name_ru": c.name_ru,
            "name_tk": c.name_tk,
            "email": c.email,
            "phone": c.phone,
            "mission_en": c.mission_en,
            "mission_ru": c.mission_ru,
            "mission_tk": c.mission_tk,
            "vision_en": c.vision_en,
            "vision_ru": c.vision_ru,
            "vision_tk": c.vision_tk,
            "address_en": c.address_en,
            "address_ru": c.address_ru,
            "address_tk": c.address_tk,
            "map_coordinates": c.map_coordinates
        }
        for c in companies
    ]
    return success_response(data, "Companies retrieved successfully")

@api_bp.route("/companies/<int:company_id>", methods=["GET"])
def get_company(company_id):
    c = get_or_404(Company, company_id)
    if isinstance(c, tuple):
        return c
    return jsonify({
        "id": c.id,
        "name_en": c.name_en,
        "name_ru": c.name_ru,
        "name_tk": c.name_tk,
        "email": c.email,
        "phone": c.phone,
        "mission_en": c.mission_en,
        "mission_ru": c.mission_ru,
        "mission_tk": c.mission_tk,
        "vision_en": c.vision_en,
        "vision_ru": c.vision_ru,
        "vision_tk": c.vision_tk,
        "address_en": c.address_en,
        "address_ru": c.address_ru,
        "address_tk": c.address_tk,
        "map_coordinates": c.map_coordinates
    })

# ---------- CERTIFICATE ----------
@api_bp.route("/certificates", methods=["GET"])
def get_certificates():
    items = Certificate.query.all()
    data = [
        {
            "id": i.id,
            "name_en": i.name_en,
            "name_ru": i.name_ru,
            "name_tk": i.name_tk,
            "description_en": i.description_en,
            "description_ru": i.description_ru,
            "description_tk": i.description_tk,
            "company_id": i.company_id
        }
        for i in items
    ]
    return success_response(data, "Certificates retrieved successfully")

@api_bp.route("/certificates/<int:item_id>", methods=["GET"])
def get_certificate(item_id):
    i = get_or_404(Certificate, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "company_id": i.company_id
    }
    return success_response(data, "Certificate retrieved successfully")

# ---------- BRAND ----------
@api_bp.route("/brands", methods=["GET"])
def get_brands():
    items = Brand.query.all()
    data = [
        {
            "id": i.id,
            "name_en": i.name_en,
            "name_ru": i.name_ru,
            "name_tk": i.name_tk,
            "subtitle_en": getattr(i, "subtitle_en", None),
            "subtitle_ru": getattr(i, "subtitle_ru", None),
            "subtitle_tk": getattr(i, "subtitle_tk", None),
            "slug": i.slug,
            "description_en": i.description_en,
            "description_ru": i.description_ru,
            "description_tk": i.description_tk,
            "company_id": i.company_id,
            "logo_image": _absolute_url(i.logo_image)
        }
        for i in items
    ]
    return success_response(data, "Brands retrieved successfully")

@api_bp.route("/brands/<int:item_id>", methods=["GET"])
def get_brand(item_id):
    i = get_or_404(Brand, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "subtitle_en": getattr(i, "subtitle_en", None),
        "subtitle_ru": getattr(i, "subtitle_ru", None),
        "subtitle_tk": getattr(i, "subtitle_tk", None),
        "slug": i.slug,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "company_id": i.company_id,
        "logo_image": _absolute_url(i.logo_image)
    }
    return success_response(data, "Brand retrieved successfully")

# ---------- BRAND by SLUG ----------
@api_bp.route("/brands/<string:slug>", methods=["GET"])
def get_brand_by_slug(slug):
    i = Brand.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Brand with slug {slug} not found", 404)
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "subtitle_en": getattr(i, "subtitle_en", None),
        "subtitle_ru": getattr(i, "subtitle_ru", None),
        "subtitle_tk": getattr(i, "subtitle_tk", None),
        "slug": i.slug,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "company_id": i.company_id,
        "logo_image": _absolute_url(i.logo_image)
    }
    return success_response(data, "Brand retrieved successfully")

# ---------- CATEGORY ----------
@api_bp.route("/categories", methods=["GET"])
def get_categories():
    items = ProductCategory.query.all()
    data = [
        {
            "id": i.id,
            "name_en": i.name_en,
            "name_ru": i.name_ru,
            "name_tk": i.name_tk,
            "slug": i.slug,
            "description_en": i.description_en,
            "description_ru": i.description_ru,
            "description_tk": i.description_tk,
            "image": i.image,
            "parent_category_id": i.parent_category_id
        }
        for i in items
    ]
    return success_response(data, "Categories retrieved successfully")

@api_bp.route("/categories/<int:item_id>", methods=["GET"])
def get_category(item_id):
    i = get_or_404(ProductCategory, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "slug": i.slug,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "image": i.image,
        "parent_category_id": i.parent_category_id
    }
    return success_response(data, "Category retrieved successfully")

# ---------- PRODUCT ----------
@api_bp.route("/products", methods=["GET"])
def get_products():
    # Filters: category (slug), brand (slug), search (in names), pagination (page, limit)
    category_slug = request.args.get("category")
    brand_slug = request.args.get("brand")
    search_query = request.args.get("search")
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        return error_response("Invalid page or limit", 400)

    query = Product.query

    if category_slug:
        category = ProductCategory.query.filter_by(slug=category_slug).first()
        if not category:
            return success_response({"products": [], "meta": {"total": 0, "current_page": 1, "last_page": 1}}, "Products retrieved successfully")
        query = query.filter(Product.category_id == category.id)

    if brand_slug:
        brand = Brand.query.filter_by(slug=brand_slug).first()
        if not brand:
            return success_response({"products": [], "meta": {"total": 0, "current_page": 1, "last_page": 1}}, "Products retrieved successfully")
        query = query.filter(Product.brand_id == brand.id)

    if search_query:
        like_expr = f"%{search_query}%"
        query = query.filter(
            (Product.name_en.ilike(like_expr)) |
            (Product.name_ru.ilike(like_expr)) |
            (Product.name_tk.ilike(like_expr))
        )

    total = query.count()
    last_page = max((total + limit - 1) // limit, 1)
    items = query.offset((page - 1) * limit).limit(limit).all()

    products = [
        {
            "id": i.id,
            "name_en": i.name_en,
            "name_ru": i.name_ru,
            "name_tk": i.name_tk,
            "slug": i.slug,
            "image": _absolute_url(i.image),
            "volume_or_weight": i.volume_or_weight,
        }
        for i in items
    ]

    data = {
        "products": products,
        "meta": {"total": total, "current_page": page, "last_page": last_page}
    }
    return success_response(data, "Products retrieved successfully")

@api_bp.route("/products/<int:item_id>", methods=["GET"])
def get_product(item_id):
    i = get_or_404(Product, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "slug": i.slug,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "volume_or_weight": i.volume_or_weight,
        "image": i.image,
        "additional_images": i.additional_images,
        "packaging_details_en": i.packaging_details_en,
        "packaging_details_ru": i.packaging_details_ru,
        "packaging_details_tk": i.packaging_details_tk,
        "category_id": i.category_id,
        "brand_id": i.brand_id
    }
    return success_response(data, "Product retrieved successfully")

# ---------- PRODUCT by SLUG ----------
@api_bp.route("/products/<string:slug>", methods=["GET"])
def get_product_by_slug(slug):
    i = Product.query.filter_by(slug=slug).first()
    if not i:
        return error_response(f"Product with slug {slug} not found", 404)
    data = {
        "id": i.id,
        "name_en": i.name_en,
        "name_ru": i.name_ru,
        "name_tk": i.name_tk,
        "slug": i.slug,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk,
        "volume_or_weight": i.volume_or_weight,
        "image": _absolute_url(i.image),
        "additional_images": [
            _absolute_url(p) for p in (i.additional_images or [])
        ],
        "packaging_details_en": i.packaging_details_en,
        "packaging_details_ru": i.packaging_details_ru,
        "packaging_details_tk": i.packaging_details_tk,
        "category": {
            "id": i.category.id,
            "name_en": i.category.name_en,
            "name_ru": i.category.name_ru,
            "name_tk": i.category.name_tk,
            "slug": i.category.slug,
        } if i.category else None,
        "brand": {
            "id": i.brand.id,
            "name_en": i.brand.name_en,
            "name_ru": i.brand.name_ru,
            "name_tk": i.brand.name_tk,
            "slug": i.brand.slug,
            "logo_image": _absolute_url(i.brand.logo_image)
        } if i.brand else None,
    }
    return success_response(data, "Product retrieved successfully")

# ---------- NEWS ----------
@api_bp.route("/news", methods=["GET"])
def get_news():
    items = News.query.all()
    data = [
        {
            "id": i.id,
            "title_en": i.title_en,
            "title_ru": i.title_ru,
            "title_tk": i.title_tk,
            "subtitle_en": getattr(i, "subtitle_en", None),
            "subtitle_ru": getattr(i, "subtitle_ru", None),
            "subtitle_tk": getattr(i, "subtitle_tk", None),
            "slug": i.slug,
            "publication_date": i.publication_date,
            "image": i.image,
            "body_text_en": i.body_text_en,
            "body_text_ru": i.body_text_ru,
            "body_text_tk": i.body_text_tk,
            "company_id": i.company_id
        }
        for i in items
    ]
    return success_response(data, "News retrieved successfully")

@api_bp.route("/news/<int:item_id>", methods=["GET"])
def get_news_item(item_id):
    i = get_or_404(News, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "title_en": i.title_en,
        "title_ru": i.title_ru,
        "title_tk": i.title_tk,
        "subtitle_en": getattr(i, "subtitle_en", None),
        "subtitle_ru": getattr(i, "subtitle_ru", None),
        "subtitle_tk": getattr(i, "subtitle_tk", None),
        "slug": i.slug,
        "publication_date": i.publication_date,
        "image": i.image,
        "body_text_en": i.body_text_en,
        "body_text_ru": i.body_text_ru,
        "body_text_tk": i.body_text_tk,
        "company_id": i.company_id
    }
    return success_response(data, "News item retrieved successfully")

# ---------- BANNER ----------
@api_bp.route("/banners", methods=["GET"])
def get_banners():
    items = Banner.query.all()
    data = [
        {
            "id": i.id,
            "image": i.image,
            "link": i.link,
            "title_en": i.title_en,
            "title_ru": i.title_ru,
            "title_tk": i.title_tk,
            "description_en": i.description_en,
            "description_ru": i.description_ru,
            "description_tk": i.description_tk
        }
        for i in items
    ]
    return success_response(data, "Banners retrieved successfully")

@api_bp.route("/banners/<int:item_id>", methods=["GET"])
def get_banner(item_id):
    i = get_or_404(Banner, item_id)
    if isinstance(i, tuple):
        return i
    data = {
        "id": i.id,
        "image": i.image,
        "link": i.link,
        "title_en": i.title_en,
        "title_ru": i.title_ru,
        "title_tk": i.title_tk,
        "description_en": i.description_en,
        "description_ru": i.description_ru,
        "description_tk": i.description_tk
    }
    return success_response(data, "Banner retrieved successfully")

# ---------- CONTACT MESSAGE (only POST) ----------
@api_bp.route("/contact_messages", methods=["POST"])
def create_contact_message():
    try:
        data = request.json
        if not data or 'message' not in data or 'email' not in data:
            return error_response("Email and message fields are required", 400)
        
        msg = ContactMessage(email=data['email'], message=data['message'])
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
