"""
Shared pytest fixtures for the integration test suite.
"""

import pytest
from starlette.testclient import TestClient

from app.main import app
from tests.fixtures.excel_factories import make_simple_xlsx

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@pytest.fixture(scope="session")
def client():
    """ASGI test client shared across the whole test session."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def clean_uploads(tmp_path, monkeypatch):
    """
    Redirect upload/output dirs to a temporary directory.

    The routes resolve Path("uploads") and Path("outputs") relative to the
    process cwd. By changing cwd to tmp_path we prevent tests from writing
    into the real backend/uploads/ directory and ensure full isolation.
    """
    (tmp_path / "uploads").mkdir()
    (tmp_path / "outputs").mkdir()
    monkeypatch.chdir(tmp_path)
    yield tmp_path


@pytest.fixture
def uploaded_file_id(client, clean_uploads):
    """Upload a minimal xlsx and return the file_id. Convenience for dependent tests."""
    xlsx = make_simple_xlsx()
    response = client.post(
        "/api/upload",
        files={"file": ("test.xlsx", xlsx, XLSX_MIME)},
    )
    assert response.status_code == 201
    return response.json()["file_id"]
