from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["success"] is True


def test_calculate_tax():
    body = {"amount": 1000000, "gender": "male", "age": 45, "location": "city"}
    response = client.post("/calculate_tax", json=body)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["tax_amount"] == 72500
