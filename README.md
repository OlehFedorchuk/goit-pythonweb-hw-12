# FastAPI Contacts REST API

## Опис проєкту

**FastAPI Contacts REST API** — це REST API застосунок для управління контактами користувачів з повною системою автентифікації, авторизації, документацією, тестуванням, Redis-кешуванням, механізмом скидання пароля та підтримкою ролей користувачів.

Проєкт реалізовано на основі **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Redis**, **JWT**, **Pytest** та **Sphinx**.

---

## Основні можливості

- Реєстрація користувача
- Авторизація користувача
- JWT Access Token
- JWT Refresh Token
- Token rotation при оновленні токенів
- Logout з інвалідацією refresh token
- Email verification
- Password reset через Redis token
- CRUD для контактів
- Ізоляція контактів між користувачами
- Ролі користувачів: `user` та `admin`
- Admin-only avatar upload
- Redis-кешування користувачів
- Sphinx-документація
- Unit та integration tests
- Покриття тестами понад 75%

---

## Технології

- Python 3.13.2
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Pydantic
- JWT / python-jose
- Passlib / bcrypt
- Pytest
- Pytest-cov
- Sphinx
- Poetry
- Cloudinary

---

## Структура проєкту

```text
.
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── auth_bearer.py
│   ├── crud.py
│   ├── database.py
│   ├── email_service.py
│   ├── redis.py
│   ├── models.py
│   ├── models_user.py
│   ├── schemas.py
│   ├── schemas_user.py
│   └── routes/
│       ├── auth.py
│       ├── contacts.py
│       └── users.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_contacts.py
│   ├── test_users.py
│   └── test_unit_crud.py
│
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── modules.rst
│   └── _build/
│       └── html/
│
├── pyproject.toml
├── poetry.lock
├── README.md
└── .env.example
```

---

## Встановлення

### 1. Клонування репозиторію

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Встановлення залежностей

```bash
poetry install
```

### 3. Активація середовища

```bash
poetry run <command>
```

---

## Змінні середовища

Створи файл `.env` у корені проєкту:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/contacts_db

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

REDIS_HOST=localhost
REDIS_PORT=6379

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_smtp_password

MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email@example.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=Contacts API
MAIL_STARTTLS=True
MAIL_SSL_TLS=False

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

> У production середовищі не зберігай `.env` у відкритому репозиторії.

---

## Запуск застосунку

```bash
poetry run uvicorn app.main:app --reload
```

Після запуску API буде доступне за адресою:

```text
http://127.0.0.1:8000
```

Swagger документація:

```text
http://127.0.0.1:8000/docs
```

ReDoc документація:

```text
http://127.0.0.1:8000/redoc
```

---

## Автентифікація

У проєкті реалізована JWT-автентифікація з двома типами токенів:

### Access Token

- Використовується для доступу до захищених API endpoints
- Час життя: 15 хвилин
- Передається у заголовку:

```http
Authorization: Bearer <access_token>
```

### Refresh Token

- Використовується для отримання нового access token
- Час життя: 7 днів
- Зберігається у Redis
- Оновлюється при кожному refresh-запиті
- Старий refresh token стає недійсним після rotation

---

## Основні endpoints

### Auth

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| POST   | `/auth/register`               | Реєстрація користувача   |
| GET    | `/auth/verify`                 | Підтвердження email      |
| POST   | `/auth/login`                  | Авторизація користувача  |
| POST   | `/auth/refresh`                | Оновлення access token   |
| POST   | `/auth/logout`                 | Вихід з акаунта          |
| POST   | `/auth/request-password-reset` | Запит на скидання пароля |
| POST   | `/auth/reset-password`         | Скидання пароля          |

---

### Users

| Method | Endpoint        | Description                            |
| ------ | --------------- | -------------------------------------- |
| GET    | `/users/me`     | Отримати профіль поточного користувача |
| PATCH  | `/users/avatar` | Завантажити avatar, тільки admin       |

---

### Contacts

| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| POST   | `/contacts/`             | Створити контакт          |
| GET    | `/contacts/`             | Отримати список контактів |
| GET    | `/contacts/{contact_id}` | Отримати контакт за ID    |
| PUT    | `/contacts/{contact_id}` | Оновити контакт           |
| DELETE | `/contacts/{contact_id}` | Видалити контакт          |

---

## Приклади запитів

### Register

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "securepassword123"
}
```

---

### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

Response:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

---

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "your_refresh_token"
}
```

Response:

```json
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer"
}
```

---

### Logout

```http
POST /auth/logout
Content-Type: application/json

{
  "refresh_token": "your_refresh_token"
}
```

Response:

```json
{
  "message": "Logged out successfully"
}
```

---

### Create Contact

```http
POST /contacts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Oleh",
  "last_name": "Fed",
  "email": "oleh@example.com",
  "phone": "+441234567890",
  "birthday": "1994-03-15",
  "additional_data": "Friend from work"
}
```

---

## Redis Implementation

Redis використовується для:

1. Кешування поточного користувача
2. Зберігання refresh tokens
3. Зберігання password reset tokens

---

### User Cache

Ключ:

```text
user:{email}
```

Дані:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "testuser",
  "role": "user"
}
```

TTL:

```text
30 minutes
```

Flow:

```text
1. User sends JWT access token
2. Token decoded
3. Email extracted from token
4. Redis checked by key user:{email}
5. If cache hit → return user from Redis
6. If cache miss → query database
7. Save user to Redis for 30 minutes
```

---

### Refresh Token Storage

Ключ:

```text
refresh_tokens:{user_id}
```

Значення:

```text
full refresh JWT token
```

TTL:

```text
8 days
```

Refresh token зберігається в Redis для можливості:

- перевірки активності токена
- logout
- token revocation
- token rotation
- invalidation after password reset

---

### Password Reset Token

Ключ:

```text
reset:{token}
```

TTL:

```text
15 minutes
```

Після успішного скидання пароля:

- пароль хешується через bcrypt
- reset token видаляється
- refresh tokens користувача інвалідовуються
- користувач має увійти знову

---

## User Roles

У системі реалізовано дві ролі:

| Role    | Description          |
| ------- | -------------------- |
| `user`  | Звичайний користувач |
| `admin` | Адміністратор        |

---

## Access Control

| Feature             | User | Admin |
| ------------------- | ---- | ----- |
| Register/Login      | Yes  | Yes   |
| View own profile    | Yes  | Yes   |
| Manage own contacts | Yes  | Yes   |
| Upload avatar       | No   | Yes   |
| Change avatar       | No   | Yes   |

---

## Admin-only Endpoint Example

```python
def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can perform this action"
        )
    return current_user
```

---

## Security Features

### Password Security

- Passwords are hashed with bcrypt
- Plain text passwords are never stored
- Password reset tokens expire after 15 minutes

### JWT Security

- Access tokens expire after 15 minutes
- Refresh tokens expire after 7 days
- Refresh tokens are stored in Redis
- Token rotation is implemented
- Logout deletes refresh token from Redis

### Email Verification

- User must verify email before login
- Verification token is sent by email

### Authorization

- Protected routes require valid access token
- Admin-only routes require admin role
- Users cannot access contacts of other users

### Database Security

- SQLAlchemy ORM prevents SQL injection
- Queries are parameterized
- User data is isolated by user ID

---

## Testing

У проєкті реалізовано 26 тестів.

### Запуск усіх тестів

```bash
poetry run pytest tests/ -v
```

### Запуск тестів з coverage

```bash
poetry run pytest tests/ -v --cov=app --cov-report=term-missing
```

### HTML coverage report

```bash
poetry run pytest tests/ --cov=app --cov-report=html
```

Після виконання команда створить папку:

```text
htmlcov/
```

Відкрий файл:

```text
htmlcov/index.html
```

---

## Test Results

```text
26 passed
0 failed
0 skipped
```

---

## Coverage Report

```text
Module                    Statements  Missing  Coverage
─────────────────────────────────────────────────────────
app/auth.py                      17       0     100%
app/auth_bearer.py               38       7      82%
app/crud.py                      56      17      70%
app/database.py                  14       4      71%
app/email_service.py             35      16      54%
app/main.py                      24       4      83%
app/models.py                    14       0     100%
app/models_user.py               11       0     100%
app/redis.py                      4       0     100%
app/routes/auth.py               83      38      54%
app/routes/contacts.py           41       4      90%
app/routes/users.py              21       0     100%
app/schemas.py                   19       0     100%
app/schemas_user.py              14       0     100%
─────────────────────────────────────────────────────────
TOTAL                           396      95      76%
```

---

## Test Files

| File                      | Description                                |
| ------------------------- | ------------------------------------------ |
| `tests/test_auth.py`      | Authentication, JWT, refresh token, logout |
| `tests/test_contacts.py`  | Contact CRUD integration tests             |
| `tests/test_users.py`     | User profile and avatar tests              |
| `tests/test_unit_crud.py` | Unit tests for CRUD functions              |
| `tests/conftest.py`       | Test fixtures, test DB, MockRedis          |

---

## Authentication Tests

Implemented tests:

- User registration
- Duplicate user registration
- Login with correct credentials
- Login with wrong password
- Login returns both access token and refresh token
- Refresh access token
- Refresh with invalid token
- Logout
- Logout with invalid token

---

## Contacts Tests

Implemented tests:

- Create contact
- Get contacts
- Get contact by ID
- Update contact
- Delete contact
- User isolation between contacts

---

## Users Tests

Implemented tests:

- Get current user profile
- Get current admin profile
- Admin avatar upload success
- Regular user avatar upload forbidden
- Unauthorized avatar upload

---

## CRUD Unit Tests

Implemented tests:

- Get contacts
- Get contact by ID
- Create contact
- Update contact
- Delete contact

---

## Sphinx Documentation

Проєкт містить повну документацію, згенеровану через Sphinx.

### Build documentation

```bash
cd docs
poetry run make html
```

або, якщо `make html` недоступний:

```bash
cd docs
poetry run sphinx-build -b html . _build/html
```

HTML документація буде згенерована у:

```text
docs/_build/html/
```

Головний файл:

```text
docs/_build/html/index.html
```

---

## Documentation Coverage

Докстрінги додано до основних модулів:

- `app/auth.py`
- `app/auth_bearer.py`
- `app/crud.py`
- `app/database.py`
- `app/email_service.py`
- `app/redis.py`
- `app/models.py`
- `app/models_user.py`
- `app/schemas.py`
- `app/schemas_user.py`
- `app/routes/auth.py`
- `app/routes/users.py`
- `app/routes/contacts.py`

---

## Docker / Redis / PostgreSQL

Якщо Redis і PostgreSQL запускаються через Docker Compose, приклад команди:

```bash
docker compose up --build
```

Перевірити контейнери:

```bash
docker ps
```

Очікувані сервіси:

```text
app
db
redis
```

---

## Useful Commands

### Run application

```bash
poetry run uvicorn app.main:app --reload
```

### Run tests

```bash
poetry run pytest tests/ -v
```

### Run tests with coverage

```bash
poetry run pytest tests/ -v --cov=app --cov-report=term-missing
```

### Build Sphinx docs

```bash
cd docs
poetry run make html
```

### Alternative Sphinx build

```bash
cd docs
poetry run sphinx-build -b html . _build/html
```

### Run Alembic migrations

```bash
poetry run alembic upgrade head
```

### Create new migration

```bash
poetry run alembic revision --autogenerate -m "migration message"
```

---

## API Response Examples

### Successful Login

```json
{
  "access_token": "access.jwt.token",
  "refresh_token": "refresh.jwt.token",
  "token_type": "bearer"
}
```

### Invalid Login

```json
{
  "detail": "Invalid credentials"
}
```

### Unauthorized Access

```json
{
  "detail": "Could not validate credentials"
}
```

### Forbidden Access

```json
{
  "detail": "Only administrators can perform this action"
}
```

### Successful Logout

```json
{
  "message": "Logged out successfully"
}
```

---

## Production Notes

Перед деплоєм потрібно перевірити:

- `SECRET_KEY` є складним і безпечним
- `.env` не додано в GitHub
- PostgreSQL використовується замість SQLite
- Redis доступний у production
- HTTPS увімкнено
- Email SMTP credentials налаштовані
- Cloudinary credentials налаштовані
- CORS налаштовано під production domain
- Debug/reload mode вимкнено

---

## Final Verification

| Requirement               | Status   |
| ------------------------- | -------- |
| Sphinx documentation      | Complete |
| Unit tests                | Complete |
| Integration tests         | Complete |
| Test coverage > 75%       | Complete |
| Redis caching             | Complete |
| Password reset            | Complete |
| User roles                | Complete |
| Admin avatar upload       | Complete |
| JWT access token          | Complete |
| JWT refresh token         | Complete |
| Token rotation            | Complete |
| Logout / token revocation | Complete |
| All tests passing         | Complete |

---

## Conclusion

Проєкт повністю реалізує всі основні вимоги:

1. REST API на FastAPI
2. Повна система автентифікації
3. JWT Access Token та Refresh Token
4. Redis-кешування
5. Password reset mechanism
6. Email verification
7. Role-based access control
8. CRUD для контактів
9. Sphinx-документація
10. Unit та integration tests
11. Test coverage 76%
12. Усі тести успішно проходять

Проєкт готовий до здачі, перевірки та подальшого розгортання.

---

## Author

**Oleh Fedorchuk**

---
