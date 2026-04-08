from fastapi.testclient import TestClient
# Importă instanța app din fișierul tău fastAPI.py
from fastAPI import app 

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200