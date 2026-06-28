import pytest
from fastapi.testclient import TestClient


def test_analytics_summary(client, test_token):
    """Тест получения сводной аналитики"""
    # Создаем несколько задач
    tasks = [
        {"title": "Задача 1", "status": "active"},
        {"title": "Задача 2", "status": "active"},
        {"title": "Задача 3", "status": "completed"},
        {"title": "Задача 4", "priority": "high"},
    ]
    for task in tasks:
        client.post(
            "/tasks/",
            headers={"Authorization": f"Bearer {test_token}"},
            json=task
        )

    # Получаем аналитику
    response = client.get(
        "/analytics/summary",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "active" in data
    assert "completed" in data
    assert "completion_rate" in data
    assert data["total"] >= 4


def test_analytics_activity(client, test_token):
    """Тест получения активности по дням"""
    # Создаем задачу
    client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Задача для активности"}
    )

    # Получаем активность за 7 дней
    response = client.get(
        "/analytics/activity?days=7",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Проверяем, что есть хотя бы одна запись
    assert len(response.json()) >= 1