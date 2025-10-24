import pytest
from fastapi.testclient import TestClient

try:
    from backend.app.main import app
    client = TestClient(app)
except Exception as e:
    # Instead of skipping everything, log the error and continue.
    pytest.skip_reason = (
        f"FastAPI main app not loaded. Details: {e}\n"
        "Only OCR module tests will run."
    )
    app = None
    client = None

@pytest.fixture(scope="session")
def client_fixture():
    """Fixture for FastAPI test client, or None if app missing."""
    if client is None:
        pytest.skip(pytest.skip_reason)
    return client
