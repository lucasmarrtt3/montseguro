# pytest

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
import pytest

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    with TestClient(app) as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao task Montseguro..."}

def test_create(client):
    response = client.post('/task-create', json={"title": "Test Title", "description": "Test Description", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"

def test_task_list(client):
    response = client.get('/task-list')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_task_update(client):
    response = client.post('/task-create', json={"title": "Test Title", "description": "Test Description", "completed": True})
    item_id = response.json()["id"]
    response = client.put(f'/task-update/{item_id}', json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json() == 'Atualizado com sucesso...'

def test_task_delete(client):
    response = client.post('/task-create', json={"title": "Test Title", "description": "Test Description", "completed": True})
    item_id = response.json()["id"]
    response = client.delete(f'/task-delete/{item_id}')
    assert response.status_code == 200
    assert response.json() == 'Excluido com sucesso...'

def test_task_search(client):
    client.post('/task-create', json={"title": "Search Test Title", "description": "Search Test Description", "completed": True})
    response = client.get('/task-search', params={"query": "Search Test Title"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_task_update_partial(client):
    response = client.post('/task-create', json={"title": "Test Title", "description": "Test Description", "completed": True})
    item_id = response.json()["id"]
    response = client.patch(f'/task-update-partial/{item_id}', json={"title": "Partially Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Partially Updated Title"

def test_task_search_by_id(client):
    response = client.post('/task-create', json={"title": "ID Search Title", "description": "ID Search Description", "completed": True})
    item_id = response.json()["id"]
    response = client.get(f'/task/{item_id}')
    assert response.status_code == 200
    assert response.json()["title"] == "ID Search Title"
    response = client.get(f'/task/{item_id}')
    assert response.status_code == 200
    assert response.json()["title"] == "ID Search Title"





