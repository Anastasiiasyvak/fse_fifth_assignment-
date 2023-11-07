import json
from fastapi.testclient import TestClient
from main import app
import httpx

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_report():
    report_data = {
        "metrics": ["dailyAverage", "weeklyAverage", "total", "min", "max"],
        "users": ["user_id1", "user_id2"]
    }
    response = client.post("/api/report/my_report", json=report_data)
    assert response.status_code == 200
    report_result = response.json()
    assert "user_id1" in report_result
    assert "user_id2" in report_result


def test_get_report():
    response = client.get("/api/report/my_report")
    assert response.status_code == 200
    report = response.json()
    assert "user_id1" in report
    assert "user_id2" in report
