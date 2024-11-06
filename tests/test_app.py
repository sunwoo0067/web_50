import pytest
from app import create_app, db
from app.models import Product, Category

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_dashboard(client):
    response = client.get('/')
    assert response.status_code == 200

def test_api_products(client):
    response = client.get('/api/products')
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json(), list)