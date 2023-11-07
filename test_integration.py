import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.integration
def test_fetch_user_data():
    response = client.get("/api/users/lastSeen?offset=20")

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

