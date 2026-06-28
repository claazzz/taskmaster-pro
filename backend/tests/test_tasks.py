import pytest
from fastapi.testclient import TestClient


def test_create_task(client, test_token):
    """Тест создания задачи"""
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "priority": "high"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Тестовая задача"
    assert response.json()["priority"] == "high"
    assert "id" in response.json()


def test_get_tasks(client, test_token):
    """Тест получения списка задач"""
    # Сначала создадим задачу
    client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Задача для списка"}
    )

    # Получаем список
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_task_by_id(client, test_token):
    """Тест получения задачи по ID"""
    # Создаем задачу
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Задача по ID"}
    )
    task_id = create_response.json()["id"]

    # Получаем её по ID
    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Задача по ID"


def test_update_task(client, test_token):
    """Тест обновления задачи"""
    # Создаем задачу
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Старое название"}
    )
    task_id = create_response.json()["id"]

    # Обновляем
    response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Новое название", "status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Новое название"
    assert response.json()["status"] == "completed"


def test_delete_task(client, test_token):
    """Тест удаления задачи"""
    # Создаем задачу
    create_response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"title": "Задача для удаления"}
    )
    task_id = create_response.json()["id"]

    # Удаляем
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 204

    # Проверяем, что задачи нет
    get_response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert get_response.status_code == 404