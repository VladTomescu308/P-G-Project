from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastAPI import app 
from database import Base, get_db

# 1. Configurare URL pentru SQLite in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. Crearea motorului de baza de date pentru test
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Crearea structurii (tabelelor) în RAM pe baza modelelor din database.py
Base.metadata.create_all(bind=engine)

# 4. Functia mock care inlocuieste conexiunea reala
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# 5. Suprascrierea dependentei globale în aplicatia FastAPI
app.dependency_overrides[get_db] = override_get_db

# Initializarea clientului de test
client = TestClient(app)

# --- SECȚIUNEA DE TESTE ---

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_identifier():
    # Testam crearea unei inregistrari pe ruta adaptata anterior
    response = client.post(
        "/identifiers/",
        json={
            "identifier_name": "TEST-001",
            "description": "Acesta este un test automatizat",
            "identifier_type": "MockType"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["identifier_name"] == "TEST-001"
    assert data["description"] == "Acesta este un test automatizat"

def test_read_identifier():
    client.post(
        "/identifiers/",
        json={"identifier_name": "TEST-002", "description": "Test citire"}
    )
    
    response = client.get("/identifiers/TEST-002")
    assert response.status_code == 200
    assert response.json()["identifier_name"] == "TEST-002"