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

def test_read_all_identifiers():
    # Testăm dacă ruta de get all returnează o listă (chiar și goală)
    response = client.get("/identifiers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_identifier_put():
    # 1. Creăm un produs de test
    client.post("/identifiers/", json={"identifier_name": "TEST-PUT", "description": "Vechi", "identifier_type": "TipVechi"})
    
    # 2. Îl suprascriem cu PUT
    response = client.put(
        "/identifiers/TEST-PUT",
        json={"identifier_name": "TEST-PUT", "description": "Nou", "identifier_type": "TipNou"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Nou"
    assert response.json()["identifier_type"] == "TipNou"

def test_update_identifier_patch():
    # 1. Creăm un produs de test
    client.post("/identifiers/", json={"identifier_name": "TEST-PATCH", "description": "Descriere originala"})
    
    # 2. Modificăm doar un singur câmp cu PATCH
    response = client.patch(
        "/identifiers/TEST-PATCH",
        json={"description": "Modificat Partial"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Modificat Partial"

def test_delete_identifier():
    # 1. Creăm produsul
    client.post("/identifiers/", json={"identifier_name": "TEST-DEL", "description": "De sters"})
    
    # 2. Îl ștergem
    response = client.delete("/identifiers/TEST-DEL")
    assert response.status_code == 200
    assert "Succes" in response.json()["message"]
    
    # 3. Verificăm că nu mai există (trebuie să primim eroare 404)
    check_response = client.get("/identifiers/TEST-DEL")
    assert check_response.status_code == 404

def test_error_404_not_found():
    # Verificăm comportamentul API-ului la cererea unui ID inexistent
    response = client.get("/identifiers/ID-CARE-NU-EXISTA-999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Identifier not found"

def test_error_duplicate_identifier():
    # Verificăm că baza de date previne duplicatele la cheia primară
    client.post("/identifiers/", json={"identifier_name": "TEST-DUP"})
    # Încercăm să îl creăm a doua oară
    response = client.post("/identifiers/", json={"identifier_name": "TEST-DUP"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Identifier already exists"