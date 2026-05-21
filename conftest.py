import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_client(client):
    # Register a test user
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123"
    })
    # Login and get token
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "email": "",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    # Return client with auth headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client