from fastapi.testclient import TestClient

from textmood_lite.api import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_post():
    response = client.post(
        "/analyze",
        json={"text": "I am so happy today"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["dominant_mood"] == "happy"
    assert "scores" in data


def test_analyze_get():
    response = client.get("/analyze?text=I%20am%20happy")
    assert response.status_code == 200
    assert response.json()["dominant_mood"] == "happy"
