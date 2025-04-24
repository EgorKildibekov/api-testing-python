import requests
from jsonschema import validate
import pytest

# Тест для получения списка пользователей
def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")  # Обратите внимание на правильный URL: reqres.in, не regres.in
    assert response.status_code == 200
    data = response.json()
    assert "data" in data  # Исправлена опечатка (было "data":)

# Схема для проверки
schema = {
    "type": "object",
    "properties": {
        "page": {"type": "number"},
        "data": {"type": "array"}
    }
}

# Тест проверки схемы ответа
def test_get_users_schema():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert validate(response.json(), schema) is None

@pytest.mark.parametrize("name, job", [("Bob", "QA"), ("Eve", "DevOps")])
def test_create_user_params(name, job):
    payload = {"name": name, "job": job}
    response = requests.post("https://reqres.in/api/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == name # Проверяем, что имя в ответе совпадает с отправленным
    assert data["job"] == job   # Проверяем, что должность в ответе совпадает с отправленной
    assert isinstance(data["id"], str) #проверяем что id строка

# Тест для проверки неверного логина
def test_invalid_login():
    payload = {"email": "test@test"}  # Нет пароля
    response = requests.post("https://reqres.in/api/login", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Missing password" # Проверяем, что сообщение об ошибке соответствует ожидаемому

# Тест для проверки несуществующего ресурса
def test_not_found():
    response = requests.get("https://reqres.in/api/users/999")
    assert response.status_code == 404

