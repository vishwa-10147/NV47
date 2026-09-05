import pytest
from fastapi.testclient import TestClient
from app.ui.web_server import app

client = TestClient(app)

def test_web_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "NV001" in response.text

def test_web_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        # Send a basic command
        websocket.send_json({"type": "command", "content": "system info"})
        
        # We should receive a log message back saying task started or kernel executing
        data = websocket.receive_json()
        assert data["type"] == "log"
