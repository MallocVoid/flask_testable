import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture(scope='session')
def app():
    app = create_app(TestingConfig)
    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()