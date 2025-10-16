import pytest
from app import schemas


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Todo API is running"


def test_create_todo_returns_201_and_created_todo(client):
    todo_data = {
        "title": "Buy milk",
        "description": "Buy milk from the market",
        "completed": False
    }

    response = client.post("/todos", json=todo_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert data["id"] == 1
