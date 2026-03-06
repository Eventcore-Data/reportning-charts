"""
Integration tests for infrastructure / smoke-test endpoints.
"""


def test_root_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Excel Chart Maker API"
    assert "version" in data
    assert "endpoints" in data
    assert "upload" in data["endpoints"]


def test_health_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
