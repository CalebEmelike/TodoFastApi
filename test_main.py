import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
from models import Todos

client = TestClient(app)

# Mocking the database session
@pytest.fixture
def mock_db_session():
    with patch('main.SessionLocal') as mock:
        mock.return_value = MagicMock()
        yield mock
        
# Test for POST /todo
def test_create_todo(mock_db_session):
    test_todo = {
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 3,
        "completed": False
    }
    response = client.post("/todo", json=test_todo)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"
    
# Test Get all todos
def test_read_all(mock_db_session):
    mock_db_session.return_value.query.return_value.all.return_value = [
        Todos(id=1, title="Test Todo", description="Test Description", priority=3, completed=False),
        Todos(id=2, title="Test Todo 2", description="Test Description 2", priority=3, completed=False)
    ]
    response = client.get("/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    
# Test Get one todo by ID
def test_read_one(mock_db_session):
    mock_db_session.return_value.query.return_value.filter.return_value.first.return_value = Todos(id=1, title="Test Todo", description="Test Description", priority=3, completed=False)
    response = client.get("/todo/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    
# Test for updating a todo
def test_upodate_todo(mock_db_session):
    updated_todo = {
        "title": "Test Todoss",
        "description": "Test Description",
        "priority": 3,
        "completed": False
    }
    response = client.put("/todo/1", json=updated_todo)
    assert response.status_code == 204
    
# Test for deleting a todo
def test_delete_todo(mock_db_session):
    response = client.delete("/todo/1")
    assert response.status_code == 204