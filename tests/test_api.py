# tests/test_api.py
import json
from app.app import app

def test_anonimize():
    client = app.test_client()
    data = [{"name": "Makoto Yuki", "persona": "Orpheus", "confidant": "SEES"}]
    response = client.post("/anonimize", json=data)
    assert response.status_code == 200
    result = json.loads(response.data)
    assert "data" in result
