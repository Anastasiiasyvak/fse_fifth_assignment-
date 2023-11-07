import pytest
import requests
import subprocess
import time

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="module")
def start_app():
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(2)

    yield

    process.terminate()


def test_read_root(start_app):
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_fetch_user_data(start_app):
    response = requests.get(f"{BASE_URL}/api/users/lastSeen?offset=20")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

