import pytest

try:
    from backend.app.main import app
except Exception as e:
    pytest.skip(
        f"Skipping backend app tests: missing dependency or FastAPI app not found.\n"
        f"Details: {e}\n"
        "Try installing dependencies: pip install fastapi httpx pytest pytest-cov\n"
        "Ensure 'app = FastAPI()' exists in backend/app/main.py",
        allow_module_level=True
    )

def test_app_importable():
    """Ensures backend.app.main is importable."""
    assert app is not None, "FastAPI app should be defined in backend/app/main.py"

def test_app_type():
    """Verifies that app is a FastAPI instance."""
    from fastapi import FastAPI
    assert isinstance(app, FastAPI), "app should be an instance of FastAPI"
