"""
Main FastAPI application module.

This module initializes the FastAPI application, configures middleware,
rate limiting, database initialization, and registers all routers.

Features:
    - CORS configuration
    - Rate limiting (SlowAPI)
    - Database initialization (SQLAlchemy)
    - Router registration (auth, users, contacts)

Modules:
    app.routes.auth
    app.routes.users
    app.routes.contacts
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import Base, engine
from app.routes import auth, contacts, users
from contextlib import asynccontextmanager

def init_db():
    """
    Initialize database tables.

    This function creates all tables defined in SQLAlchemy models
    using the configured database engine.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)


app = FastAPI()

@asynccontextmanager

async def lifespan(app: FastAPI):

    init_db()

    yield

app = FastAPI(lifespan=lifespan)
limiter = Limiter(
    key_func=get_remote_address
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(users.router)

@app.get("/")
def root():
    """
    Health check endpoint.

    Returns:
        dict: Simple API status message.
    """
    return {
        "message": "API works"
    }