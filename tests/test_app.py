import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_for_activity_duplicate():
    # Try to sign up the same user again
    client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=testuser@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant_success():
    # First, sign up a user
    client.post("/activities/Chess Club/signup?email=deleteuser@mergington.edu")
    # Then, unregister
    response = client.post("/unregister", json={"activity": "Chess Club", "participant": "deleteuser@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_unregister_participant_not_found():
    response = client.post("/unregister", json={"activity": "Chess Club", "participant": "notfound@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Participant not found" in response.json()["error"]


def test_unregister_activity_not_found():
    response = client.post("/unregister", json={"activity": "Nonexistent", "participant": "someone@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "Activity not found" in response.json()["error"]
