"""
Integration tests for GET /api/chart/{file_id} (direct binary download).
"""

MISSING_FILE_ID = "00000000-0000-0000-0000-000000000000"

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
PDF_HEADER = b"%PDF"


def test_download_returns_png_bytes(client, uploaded_file_id):
    response = client.get(f"/api/chart/{uploaded_file_id}?format=png&chart_type=bar")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert "attachment" in response.headers["content-disposition"]
    assert "chart.png" in response.headers["content-disposition"]
    assert response.content[:8] == PNG_HEADER


def test_download_returns_svg(client, uploaded_file_id):
    response = client.get(f"/api/chart/{uploaded_file_id}?format=svg&chart_type=bar")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert b"<svg" in response.content


def test_download_returns_pdf(client, uploaded_file_id):
    response = client.get(f"/api/chart/{uploaded_file_id}?format=pdf&chart_type=bar")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content[:4] == PDF_HEADER


def test_download_missing_file_id_returns_404(client):
    response = client.get(f"/api/chart/{MISSING_FILE_ID}")
    assert response.status_code == 404


def test_download_with_custom_title(client, uploaded_file_id):
    response = client.get(f"/api/chart/{uploaded_file_id}?format=png&title=MyChart")
    assert response.status_code == 200
    assert response.content[:8] == PNG_HEADER


def test_download_with_grid_params(client, uploaded_file_id):
    url = (
        f"/api/chart/{uploaded_file_id}"
        "?format=png&grid_enabled=true&grid_linestyle=dashed&grid_alpha=0.5"
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.content[:8] == PNG_HEADER
