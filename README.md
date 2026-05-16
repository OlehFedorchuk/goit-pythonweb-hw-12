# 📦 FastAPI Contacts API

REST API для управління контактами з JWT авторизацією, верифікацією email та завантаженням аватарів через Cloudinary.

---

## 🚀 Features

- 🔐 JWT Authentication (register / login)
- 📧 Email verification (Gmail SMTP)
- 👤 User profile (`/users/me`)
- 📇 Contacts CRUD API
- 🖼️ Avatar upload via Cloudinary
- 🐘 PostgreSQL database
- 🐳 Docker + Docker Compose
- 🌐 CORS enabled

---

## 🧱 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT (python-jose)
- Passlib (bcrypt)
- Cloudinary
- Docker

---

## 📁 Project Structure

bash

```
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── app
    ├── main.py
    ├── database.py
    ├── crud.py
    ├── auth.py
    ├── auth_bearer.py
    ├── email_service.py
    ├── cloudinary_service.py
    ├── models.py
    ├── models_user.py
    ├── schemas.py
    ├── schemas_user.py
    └── routes
        ├── auth.py
        ├── users.py
        └── contacts.py
```

## ⚙️ Environment Variables

bash

```
Create .env file:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=postgres
DATABASE_URL=postgresql://postgres:password@db:5432/postgres

SECRET_KEY=your_super_secret_key
ALGORITHM=HS256

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_google_app_password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

```

## 🐳 Run with Docker

bash

```
docker-compose up --build
```

bash

```
docker-compose down
```

## 🔐 Authentication Flow

bash

```
POST /auth/register
POST /auth/login

GET /users/me
PATCH /users/avatar

GET /contacts/
POST /contacts/
GET /contacts/{id}
PUT /contacts/{id}
DELETE /contacts/{id}
```

## 📧 Email Verification

```
Register → email → verify → activate account
```

## ☁️ Cloudinary

```
Used for avatar uploads
```
