from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_and_whoami():
    r = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r2 = client.get("/whoami", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.json()["user"] == "admin"
