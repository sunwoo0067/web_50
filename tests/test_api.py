import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_search(client):
    response = client.post('/search', data={'query': 'test'})
    assert response.status_code == 200
    # 추가적인 응답 내용 검증 