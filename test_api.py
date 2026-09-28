from fastapi.testclient import TestClient
import backend.routes as routes
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_generate(monkeypatch):
    class FakeGenerator:
        model = "test-model"
        def __init__(self): pass
        def generate_document(self, **kwargs): return "TEST LEGAL DOCUMENT\n\n1. Terms\nSample clause."
    monkeypatch.setattr(routes, "GeminiDocumentGenerator", FakeGenerator)
    response = client.post("/generate", json={"document_type":"NDA","parties":"A (Disclosing Party), B (Receiving Party)","terms":["Confidentiality"],"effective_date":"2026-09-26","language":"English","additional_instructions":""})
    assert response.status_code == 200
    assert response.json()["document_type"] == "NDA"
    assert "TEST LEGAL DOCUMENT" in response.json()["content"]
