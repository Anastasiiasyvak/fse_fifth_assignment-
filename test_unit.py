import json
from fastapi.testclient import TestClient
from main import app
import requests

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404


def test_create_report():
    report_data = {
        "metrics": ["dailyAverage", "weeklyAverage", "total", "min", "max"],
        "users": ["fe2c6cb3-296f-d4a9-16dc-a2c3500b1d98", "5ca3c3fc-c842-9f4e-fa1f-028b96e06515"]
    }
    response = client.post("/api/report/my_report", json=report_data)
    assert response.status_code == 200
    report_result = response.json()
    assert "fe2c6cb3-296f-d4a9-16dc-a2c3500b1d98" in report_result
    assert "5ca3c3fc-c842-9f4e-fa1f-028b96e06515" in report_result


