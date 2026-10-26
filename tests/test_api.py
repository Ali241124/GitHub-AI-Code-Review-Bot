
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "GitHub AI Code Review Bot is running"
    )


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model"] == "qwen2.5:7b"


def test_review_rejects_empty_code():
    response = client.post(
        "/review",
        json={
            "language": "python",
            "code": "",
        },
    )

    assert response.status_code == 422


def test_review_rejects_missing_code():
    response = client.post(
        "/review",
        json={
            "language": "python",
        },
    )

    assert response.status_code == 422
