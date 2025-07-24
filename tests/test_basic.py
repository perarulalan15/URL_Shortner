# tests/test_basic.py

import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_shorten_valid_url(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400

def test_redirect_and_stats(client):
    # Shorten URL
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    data = res.get_json()
    short_code = data["short_code"]

    # Redirect
    res_redirect = client.get(f"/{short_code}")
    assert res_redirect.status_code == 302

    # Stats
    res_stats = client.get(f"/api/stats/{short_code}")
    stats = res_stats.get_json()
    assert stats["url"] == "https://example.com"
    assert stats["clicks"] == 1
