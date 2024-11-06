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

def test_database_initialization(app):
    with app.app_context():
        assert db.engine.table_names() == ['categories', 'products']

def test_product_creation(app):
    with app.app_context():
        category = Category(name="Electronics")
        db.session.add(category)
        db.session.commit()

        product = Product(name="Laptop")
        db.session.add(product)
        db.session.commit()

        assert db.engine.table_names() == ['categories', 'products']
        assert Product.query.filter_by(name="Laptop").first() is not None 