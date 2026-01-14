# tests/test_websocket.py
from typing import Any, Dict

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_websocket_server_info() -> None:
    """
    Sprawdza, czy WebSocket zwraca poprawny JSON ze statusem i datą.
    """
    with client.websocket_connect("/ws/server-info") as websocket:
        data: Dict[str, Any] = websocket.receive_json()
        assert data["status"] == "ok"
        assert "datetime" in data