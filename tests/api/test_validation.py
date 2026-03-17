from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ask_endpoint_rejects_empty_question():
    # Empty string should fail due to min_length=1
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422


def test_ask_endpoint_rejects_whitespace_only_question():
    # Whitespace only should fail due to strip_whitespace=True & min_length=1
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422


def test_ask_endpoint_rejects_missing_question_field():
    # Missing required field
    response = client.post("/ask", json={})
    assert response.status_code == 422
