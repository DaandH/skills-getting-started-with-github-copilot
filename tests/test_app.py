from fastapi.testclient import TestClient
import uuid

from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # ensure one of the seeded activities is present
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = f"test+{uuid.uuid4().hex[:8]}@example.com"

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant appears in activity
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    participants = resp2.json()[activity]["participants"]
    assert email in participants

    # Unregister the participant
    resp3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp3.status_code == 200
    assert "Unregistered" in resp3.json().get("message", "")

    # Confirm removal
    resp4 = client.get("/activities")
    participants2 = resp4.json()[activity]["participants"]
    assert email not in participants2


def test_unregister_nonexistent_returns_404():
    activity = "Chess Club"
    email = f"notfound+{uuid.uuid4().hex[:8]}@example.com"
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 404
