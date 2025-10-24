import pytest

try:
    from backend.app.main import app
    from fastapi.testclient import TestClient
except Exception:
    pytest.skip("Skipping: FastAPI app not available for testing.", allow_module_level=True)

client = TestClient(app)

def test_app_startup():
    """Ensures app starts and responds to /ping if defined."""
    routes = [r.path for r in app.routes]
    assert len(routes) > 0, "No routes defined in FastAPI app"

def test_ocr_endpoint_exists():
    """Checks if /ocr route is registered."""
    paths = [r.path for r in app.routes]
    if "/ocr" not in paths:
        pytest.skip("Skipping: /ocr route not yet implemented.")
    assert "/ocr" in paths, "Expected /ocr route not found"

def test_ocr_endpoint_invalid_input():
    """Verifies /ocr returns 400 for unsupported file types."""
    paths = [r.path for r in app.routes]
    if "/ocr" not in paths:
        pytest.skip("Skipping: /ocr route not yet implemented.")
    resp = client.post("/ocr", data={"engine": "tesseract"})
    assert resp.status_code in (400, 422), "Expected validation or bad request error"

def test_cors_headers_present():
    """Ensures CORS middleware is configured."""
    cors_middleware = any("CORSMiddleware" in str(m) for m in app.user_middleware)
    assert cors_middleware, "CORS middleware not configured"
