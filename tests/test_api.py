import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "service" in data


def test_research_endpoint_validation():
    """Test research endpoint with invalid data"""
    # Test with missing topic
    response = client.post("/research", json={})
    assert response.status_code == 422
    
    # Test with too short topic
    response = client.post("/research", json={"topic": "AI"})
    assert response.status_code == 422
    
    # Test with invalid depth
    response = client.post("/research", json={
        "topic": "Test topic",
        "depth": 10  # Max is 5
    })
    assert response.status_code == 422


def test_history_endpoint():
    """Test history endpoint"""
    response = client.get("/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "limit" in data
    assert "research" in data
    assert isinstance(data["research"], list)


def test_invalid_research_id():
    """Test getting non-existent research"""
    response = client.get("/research/invalid_id_12345")
    # Should return 404 or 500 depending on implementation
    assert response.status_code in [404, 500]


def test_report_endpoint_validation():
    """Test report endpoint with invalid data"""
    # Test with missing research_id
    response = client.post("/report", json={})
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
