"""
Integration tests for POST /api/chart-data.
"""

import pytest

from tests.fixtures.excel_factories import (
    make_multi_section_xlsx,
    make_percentage_xlsx,
    make_pie_xlsx,
    make_ratings_xlsx,
    make_scatter_xlsx,
    make_simple_xlsx,
)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
MISSING_FILE_ID = "00000000-0000-0000-0000-000000000000"


def _upload(client, clean_uploads, xlsx_bytes, filename="test.xlsx"):
    resp = client.post(
        "/api/upload",
        files={"file": (filename, xlsx_bytes, XLSX_MIME)},
    )
    assert resp.status_code == 201
    return resp.json()["file_id"]


def test_chart_data_line_type(client, uploaded_file_id):
    response = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "line", "theme": "professional"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_type"] == "line"
    assert len(body["traces"]) >= 1
    assert body["traces"][0]["type"] == "scatter"
    assert body["traces"][0]["mode"] == "lines+markers"
    assert isinstance(body["columns"], list)
    assert "layout" in body


def test_chart_data_bar_type(client, uploaded_file_id):
    response = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "bar"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_type"] == "bar"
    assert body["traces"][0]["type"] == "bar"


def test_chart_data_horizontal_bar(client, clean_uploads):
    xlsx = make_simple_xlsx(
        headers=("Category", "Score"),
        rows=[("A", 4.2), ("B", 3.1), ("C", 3.9)],
    )
    file_id = _upload(client, clean_uploads, xlsx)
    response = client.post(
        "/api/chart-data",
        json={"file_id": file_id, "chart_type": "horizontal_bar"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_type"] == "horizontal_bar"
    assert body["traces"][0].get("orientation") == "h"


def test_chart_data_scatter_type(client, clean_uploads):
    xlsx = make_scatter_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "scatter.xlsx")
    response = client.post(
        "/api/chart-data",
        json={"file_id": file_id, "chart_type": "scatter"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["chart_type"] == "scatter"
    assert body["traces"][0]["mode"] == "markers"


def test_chart_data_pie_type(client, clean_uploads):
    xlsx = make_pie_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "pie.xlsx")
    response = client.post(
        "/api/chart-data",
        json={"file_id": file_id, "chart_type": "pie"},
    )
    assert response.status_code == 200
    assert response.json()["traces"][0]["type"] == "pie"


def test_chart_data_auto_line_for_multicolumn(client, uploaded_file_id):
    response = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "auto"},
    )
    assert response.status_code == 200
    assert response.json()["chart_type"] == "line"


def test_chart_data_auto_horizontal_bar_for_percentage(client, clean_uploads):
    xlsx = make_percentage_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "pct.xlsx")
    response = client.post(
        "/api/chart-data",
        json={"file_id": file_id, "chart_type": "auto"},
    )
    assert response.status_code == 200
    assert response.json()["chart_type"] == "horizontal_bar"


def test_chart_data_missing_file_id_returns_404(client):
    response = client.post(
        "/api/chart-data",
        json={"file_id": MISSING_FILE_ID, "chart_type": "line"},
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_chart_data_missing_field_returns_422(client):
    # file_id is required — omitting it triggers Pydantic 422
    response = client.post("/api/chart-data", json={"chart_type": "bar"})
    assert response.status_code == 422


def test_chart_data_custom_title_in_layout(client, uploaded_file_id):
    response = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "title": "My Custom Title"},
    )
    assert response.status_code == 200
    assert "My Custom Title" in response.json()["layout"]["title"]["text"]


def test_chart_data_theme_changes_colorway(client, uploaded_file_id):
    r_pro = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "theme": "professional"},
    )
    r_vib = client.post(
        "/api/chart-data",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "theme": "vibrant"},
    )
    assert r_pro.status_code == 200
    assert r_vib.status_code == 200
    assert r_pro.json()["layout"]["colorway"] != r_vib.json()["layout"]["colorway"]


def test_chart_data_ratings_mode_per_bar_colors(client, clean_uploads):
    xlsx = make_ratings_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "ratings.xlsx")
    response = client.post(
        "/api/chart-data",
        json={
            "file_id": file_id,
            "chart_type": "horizontal_bar",
            "ratings_mode": True,
            "ratings_low_threshold": 3.15,
            "ratings_high_threshold": 3.85,
        },
    )
    assert response.status_code == 200
    trace = response.json()["traces"][0]
    colors = trace["marker"]["color"]
    assert isinstance(colors, list), "ratings_mode should produce per-bar color list"
    assert colors[0] == "#E8483B"   # 3.0 <= 3.15 → red
    assert colors[2] == "#4CAF50"   # 4.0 > 3.85 → green


def test_chart_data_multi_section_section_index(client, clean_uploads):
    xlsx = make_multi_section_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "multi.xlsx")
    for i in [0, 1]:
        response = client.post(
            "/api/chart-data",
            json={"file_id": file_id, "chart_type": "bar", "section_index": i},
        )
        assert response.status_code == 200, f"section_index={i} failed"
        assert len(response.json()["traces"]) > 0
