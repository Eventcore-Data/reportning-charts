"""
Integration tests for DELETE /api/cleanup/{file_id}.
"""

from tests.fixtures.excel_factories import make_simple_xlsx

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _upload(client, xlsx_bytes=None, filename="del.xlsx"):
    if xlsx_bytes is None:
        xlsx_bytes = make_simple_xlsx()
    resp = client.post(
        "/api/upload",
        files={"file": (filename, xlsx_bytes, XLSX_MIME)},
    )
    assert resp.status_code == 201
    return resp.json()["file_id"]


def test_cleanup_deletes_uploaded_file(client, clean_uploads):
    file_id = _upload(client)
    upload_path = clean_uploads / "uploads" / f"{file_id}.xlsx"
    assert upload_path.exists()

    response = client.delete(f"/api/cleanup/{file_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Files deleted successfully"
    assert any(file_id in f for f in body["deleted_files"])
    assert not upload_path.exists()


def test_cleanup_nonexistent_returns_404(client, clean_uploads):
    response = client.delete("/api/cleanup/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert "No files found" in response.json()["detail"]


def test_cleanup_idempotency(client, clean_uploads):
    """A second cleanup of the same file_id returns 404, not a 500."""
    file_id = _upload(client)
    client.delete(f"/api/cleanup/{file_id}")
    response = client.delete(f"/api/cleanup/{file_id}")
    assert response.status_code == 404
