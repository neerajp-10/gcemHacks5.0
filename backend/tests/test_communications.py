"""Unit tests for Twilio Agri-Communications and low-bandwidth telephony endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_communications_status():
    """Verify provider status endpoint returns configuration and supported languages."""
    response = client.get("/api/communications/status")
    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert "supported_languages" in data
    assert "kn" in data["supported_languages"]
    assert "hi" in data["supported_languages"]
    assert "en" in data["supported_languages"]


def test_dispatch_sms_simulation():
    """Verify SMS dispatch returns valid telecom simulation payload with correct phone number."""
    payload = {
        "to": "+919731803808",
        "farm_id": "mandya",
        "language": "kn",
    }
    response = client.post("/api/communications/sms", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["to"] == "+919731803808"
    assert data["language"] == "kn"
    assert "sid" in data
    assert data["segments"] >= 1


def test_dispatch_call_simulation():
    """Verify IVR voice call simulation returns valid TwiML and voice attributes."""
    payload = {
        "to": "+919731803808",
        "farm_id": "mandya",
        "language": "kn",
    }
    response = client.post("/api/communications/call", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["to"] == "+919731803808"
    assert "Google.kn-IN" in data["voice_engine"]
    assert "twiml" in data
    assert "<Say" in data["twiml"]


def test_dispatch_low_bandwidth_unified():
    """Verify headless low-bandwidth dispatch works for cellular delivery."""
    payload = {
        "to": "+919731803808",
        "farm_id": "mandya",
        "language": "kn",
        "channel": "both",
    }
    response = client.post("/api/communications/dispatch-low-bandwidth", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["farmer_phone"] == "+919731803808"
    assert data["sms_dispatch"] is not None
    assert data["voice_call_dispatch"] is not None
    assert "GSM/PSTN" in data["low_bandwidth_notice"]


def test_inbound_voice_call_helpline_twiml():
    """Verify inbound missed-call/IVR dial-in returns proper TwiML audio response."""
    response = client.post("/api/communications/incoming-call?From=%2B919731803808&farm_id=mandya&language=kn")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert "<Response>" in response.text
    assert "<Say voice=" in response.text


def test_inbound_sms_helpline_twiml():
    """Verify inbound farmer SMS query returns automated 160-char SMS response TwiML."""
    response = client.post("/api/communications/incoming-sms?From=%2B919731803808&Body=mandya")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert "<Response>" in response.text
    assert "<Message>" in response.text


def test_twiml_endpoint():
    """Verify GET /api/communications/twiml generates valid voice XML."""
    response = client.get("/api/communications/twiml?script=Test&language=en")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert "<Say" in response.text
