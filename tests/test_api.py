from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_valid_url():
    response = client.post(
        "/audit",
        json={"url": "https://example.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert data["data"]["status_code"] == 200
    assert data["data"]["title"] == "Example Domain"

def test_invalid_url():

    response = client.post(
        "/audit",
        json={"url": "invalid-url"}
    )

    assert response.status_code == 422