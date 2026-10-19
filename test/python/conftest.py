"""Shared pytest fixtures and configuration for Domoticz Python test suite.

These tests are designed to be self-contained and CI-friendly:
- Static analysis tests (command_rights, oauth2 splitting) need NO running server.
- Dynamic tests (api_sweep, calibration, plugin_websocket) require a running
  Domoticz instance and are skipped automatically when none is available.
"""

import os
import socket
import pytest


def _domoticz_running(host: str = "127.0.0.1", port: int = 8080, timeout: float = 1.0) -> bool:
    """Check if a Domoticz instance is reachable."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (OSError, ConnectionRefusedError):
        return False


@pytest.fixture(scope="session")
def domoticz_available():
    """Session-scoped fixture: is a running Domoticz available?"""
    host = os.environ.get("DOMOTICZ_HOST", "127.0.0.1")
    port = int(os.environ.get("DOMOTICZ_PORT", "8080"))
    if not _domoticz_running(host, port):
        pytest.skip(
            f"No Domoticz running at {host}:{port} — "
            "set DOMOTICZ_HOST/DOMOTICZ_PORT or start a local instance"
        )
    return {"host": host, "port": port}


@pytest.fixture(scope="session")
def domoticz_base_url(domoticz_available):
    """Base URL for the running Domoticz instance."""
    info = domoticz_available
    return f"http://{info['host']}:{info['port']}"
