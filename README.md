# FastAPI Contacts REST API

## Опис проєкту

**FastAPI Contacts REST API** — це REST API застосунок для управління контактами користувачів з повною системою автентифікації, авторизації, документацією, тестуванням, Redis-кешуванням, механізмом скидання пароля та підтримкою ролей користувачів.

Проєкт реалізовано на основі **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Redis**, **JWT**, **Pytest** та **Sphinx**.

---

## Статус проєкту

**Status:** Complete  
**Date:** May 16, 2026  
**Tests:** 26/26 Passed  
**Coverage:** 76%  
**Documentation:** Sphinx HTML documentation generated successfully

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
│   ├── __init__.py
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
│       ├── __init__.py
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
├── alembic/
├── pyproject.toml
├── poetry.lock
├── README.md
└── .env
```
