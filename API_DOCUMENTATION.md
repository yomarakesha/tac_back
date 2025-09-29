  # 📑 API Документация

  ## Общая информация
  - **Базовый URL**: `http://<host>/api/`
  - **Формат данных**: JSON

  ### Структура ответа
  **Успех**
  ```json
  {
    "success": true,
    "message": "Описание операции",
    "data": {...}
  }
  ```

  **Ошибка**
  ```json
  {
    "success": false,
    "message": "Описание ошибки"
  }
  ```

  ---

  ## 🔹 Companies

  | Метод | Путь                 | Описание                    | Параметры |
  |-------|----------------------|-----------------------------|-----------|
  | GET   | `/companies`         | Получить список компаний    | –         |
  | GET   | `/companies/<id>`    | Получить компанию по ID     | `id` – int |

  **Пример ответа**
  ```json
  {
    "success": true,
    "message": "Companies retrieved successfully",
    "data": [
      {
        "id": 1,
        "name_en": "Company EN",
        "email": "info@example.com"
      }
    ]
  }
  ```

  ---

  ## 🔹 Certificates

  | Метод | Путь                         | Описание                  | Параметры |
  |-------|------------------------------|---------------------------|-----------|
  | GET   | `/certificates`              | Список сертификатов       | –         |
  | GET   | `/certificates/<id>`         | Сертификат по ID          | `id` – int |
  | GET   | `/certificates/<slug>`       | Сертификат по slug        | `slug` – str |

  **Пример**
  ```json
  {
    "success": true,
    "message": "Certificates retrieved successfully",
    "data": [
      {
        "id": 1,
        "image": "http://host/static/uploads/cert1.png",
        "slug": "iso-9001"
      }
    ]
  }
  ```

  ---

  ## 🔹 Brands

  | Метод | Путь                  | Описание             | Параметры   |
  |-------|-----------------------|----------------------|-------------|
  | GET   | `/brands`             | Список брендов       | –           |
  | GET   | `/brands/<id>`        | Бренд по ID          | `id` – int  |
  | GET   | `/brands/<slug>`      | Бренд по slug        | `slug` – str |

  **Пример**
  ```json
  {
    "success": true,
    "message": "Brand retrieved successfully",
    "data": {
      "id": 5,
      "name_en": "Brand EN",
      "slug": "brand-slug"
    }
  }
  ```

  ---

  ## 🔹 Categories

  | Метод | Путь                     | Описание                           | Параметры   |
  |-------|--------------------------|------------------------------------|-------------|
  | GET   | `/categories`            | Все категории                      | –           |
  | GET   | `/categories/parents`    | Только родительские категории      | –           |
  | GET   | `/categories/<id>`       | Категория по ID                    | `id` – int  |

  **Пример**
  ```json
  {
    "success": true,
    "message": "Category retrieved successfully",
    "data": {
      "id": 2,
      "name_en": "Beverages",
      "slug": "beverages"
    }
  }
  ```

  ---

  ## 🔹 Products

  | Метод | Путь                                  | Описание                                   | Параметры (query) |
  |-------|---------------------------------------|--------------------------------------------|-------------------|
  | GET   | `/products`                           | Список товаров с фильтрацией и пагинацией  | `category_id`, `category`, `q`, `page`, `limit` |
  | GET   | `/products/<id>`                      | Товар по ID                                | `id` – int        |
  | GET   | `/products/<slug>`                    | Товар по slug                              | `slug` – str      |
  | GET   | `/products/recommendations/<exclude>` | 3 случайных товара, кроме указанного ID    | `exclude` – int   |

  **Пример**
  ```json
  {
    "success": true,
    "message": "Products retrieved successfully",
    "data": {
      "products": [
        {
          "id": 10,
          "name_en": "Coca Cola",
          "slug": "coca-cola"
        }
      ],
      "meta": {
        "total": 15,
        "current_page": 1,
        "last_page": 8
      }
    }
  }
  ```

  ---

  ## 🔹 News

  | Метод | Путь                              | Описание                          | Параметры |
  |-------|-----------------------------------|-----------------------------------|-----------|
  | GET   | `/news`                           | Список новостей с пагинацией      | `page`, `limit` |
  | GET   | `/news/<id>`                      | Новость по ID                     | `id` – int |
  | GET   | `/news/<slug>`                    | Новость по slug                   | `slug` – str |
  | GET   | `/news/recommendations/<exclude>` | 3 случайные новости, кроме указанной | `exclude` – int |

  **Пример**
  ```json
  {
    "success": true,
    "message": "News retrieved successfully",
    "data": {
      "news": [
        {
          "id": 3,
          "title_en": "Company opens new plant",
          "slug": "new-plant"
        }
      ],
      "meta": {
        "total": 42,
        "current_page": 1,
        "last_page": 3
      }
    }
  }
  ```

  ---

  ## 🔹 Banners

  | Метод | Путь                | Описание        | Параметры   |
  |-------|---------------------|-----------------|-------------|
  | GET   | `/banners`          | Список баннеров | –           |
  | GET   | `/banners/<id>`     | Баннер по ID    | `id` – int  |
  | GET   | `/banners/<slug>`   | Баннер по slug  | `slug` – str |

  **Пример**
  ```json
  {
    "success": true,
    "message": "Banner retrieved successfully",
    "data": {
      "id": 7,
      "image": "http://host/static/banners/sale.png",
      "link": "http://example.com/promo",
      "slug": "autumn-sale"
    }
  }
  ```

  ---

  ## 🔹 Contact Messages

  | Метод | Путь                 | Описание                        | Параметры (body) |
  |-------|----------------------|---------------------------------|------------------|
  | POST  | `/contact_messages`  | Создать сообщение обратной связи | `name`, `email`, `message` |

  **Пример запроса**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, I want to ask about your products."
  }
  ```

  **Пример ответа**
  ```json
  {
    "success": true,
    "message": "Contact message created successfully",
    "data": {"id": 12}
  }
  ```

  ---

  ## 🔹 Newsletter Subscribers

  | Метод | Путь                       | Описание               | Параметры (body) |
  |-------|----------------------------|------------------------|------------------|
  | POST  | `/newsletter_subscribers`  | Подписка на рассылку   | `email`          |

  **Пример запроса**
  ```json
  {
    "email": "subscriber@example.com"
  }
  ```

  **Ответ при новом email**
  ```json
  {
    "success": true,
    "message": "Newsletter subscriber created successfully",
    "data": {"id": 34}
  }
  ```

  **Ответ при существующем email**
  ```json
  {
    "success": true,
    "message": "Already subscribed",
    "data": {"id": 34}
  }
  ```
