import pytest

from app import create_app
from extensions import db


@pytest.fixture
def app():
    app = create_app()

    # Use a separate temporary database for testing.
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SECRET_KEY="test-secret-key",
        JWT_SECRET_KEY="test-jwt-secret-key"
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
