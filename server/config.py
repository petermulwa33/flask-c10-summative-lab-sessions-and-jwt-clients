
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///notes.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY",
        "development-jwt-secret"
    )
