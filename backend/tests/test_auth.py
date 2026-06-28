import pytest
from fastapi.testclient import TestClient

def test_register_success(client):
    """Тест успешной регистрации"""
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "newpass123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "new@example.com"

def test_register_duplicate_username(client, test_user):
    """Тест регистрации с существующим логином"""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "another@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 400
    assert "существует" in response.json()["detail"]

def test_login_success(client, test_user):
    """Тест успешного входа"""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Тест входа с неверным паролем"""
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Неверный" in response.json()["detail"]