import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):      #it tests the health check endpoint
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url(client):      #it tests the shorten url endpoint
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data
    return data["short_code"]

def test_redirect_and_analytics(client):      #it tests the redirect and analytics endpoint
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    assert response.status_code == 201
    data = response.get_json()
    code = data["short_code"]
    for i in range(3):
        r = client.get(f'/{code}', follow_redirects=False)
        assert r.status_code == 302
        assert r.headers["Location"] == "https://www.example.com"
    stats = client.get(f'/api/stats/{code}')
    assert stats.status_code == 200
    stats_data = stats.get_json()
    assert stats_data["url"] == "https://www.example.com"
    assert stats_data["clicks"] == 3
    assert "created_at" in stats_data

def test_invalid_url(client):      #here we test the invalid url endpoint
    response = client.post('/api/shorten', json={"url": "not-a-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_missing_url(client):      #here we test the missing url endpoint
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_not_found(client):      #testing the not found endpoint
    r = client.get('/notarealcode')
    assert r.status_code == 404
    stats = client.get('/api/stats/notarealcode')
    assert stats.status_code == 404
    stats_data = stats.get_json()
    assert "error" in stats_data