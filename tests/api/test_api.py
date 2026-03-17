from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ask_endpoint():
    response = client.post("/ask", json={"question": "O que é LGPD?"})
    assert response.status_code == 200
    assert "answer" in response.json()
