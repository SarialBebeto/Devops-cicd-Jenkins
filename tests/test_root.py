import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import database

client = TestClient(app)

@pytest.fixture(autouse=True, scope="module")
def setup_and_teardown():
    # this runs before and after all tests in this file
    with TestClient(app) as test_client:
        yield test_client  # this is where the testing happens

def test_root_returns_users(setup_and_teardown):
    response = setup_and_teardown.get("/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(u["email"] == "test@test.com" for u in users)

def test_startup_creates_user(setup_and_teardown):
    response = setup_and_teardown.get("/")
    assert response.status_code == 200
    users = response.json()
    emails = [user["email"] for user in users]
    assert "test@test.com" in emails

