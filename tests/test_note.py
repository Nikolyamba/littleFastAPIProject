from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from database.session import Base, get_db
from main import app

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_get_notes():
    response = client.get('/notes')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_note():
    response = client.post('/notes', json={'title': 'a', 'context': 'tralala'})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == 'a'
    assert data["context"] == 'tralala'
    assert 'created_at' in data

def test_bad_get_note():
    response = client.get('/notes/0')
    assert response.status_code == 500
