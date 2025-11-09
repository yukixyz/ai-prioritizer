from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_predict():
    payload = {
        "id":"t1",
        "asset":"web",
        "asset_criticality":"high",
        "cvss":9.0,
        "summary":"sql injection",
        "description":"parameter not sanitized",
        "remediation":"use prepared statements"
    }
    r = client.post('/predict', json=payload)
    assert r.status_code == 200
    j = r.json()
    assert 'score' in j
    assert 'priority' in j
