"""
Integration tests for POST /api/generate.
"""

import base64

import pytest

from tests.fixtures.excel_factories import (
    make_pie_xlsx,
    make_scatter_xlsx,
    make_simple_xlsx,
)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
MISSING_FILE_ID = "00000000-0000-0000-0000-000000000000"

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
PDF_HEADER = b"%PDF"


def _upload(client, clean_uploads, xlsx_bytes, filename="test.xlsx"):
    resp = client.post(
        "/api/upload",
        files={"file": (filename, xlsx_bytes, XLSX_MIME)},
    )
    assert resp.status_code == 201
    return resp.json()["file_id"]


def test_generate_returns_base64_png(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "format": "png"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "chart_base64" in body
    assert body["format"] == "png"
    assert body["filename"].endswith("_chart.png")
    decoded = base64.b64decode(body["chart_base64"])
    assert decoded[:8] == PNG_HEADER


def test_generate_returns_base64_svg(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "format": "svg"},
    )
    assert response.status_code == 200
    decoded = base64.b64decode(response.json()["chart_base64"]).decode("utf-8")
    assert "<svg" in decoded


def test_generate_returns_base64_pdf(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "format": "pdf"},
    )
    assert response.status_code == 200
    decoded = base64.b64decode(response.json()["chart_base64"])
    assert decoded[:4] == PDF_HEADER


@pytest.mark.parametrize("chart_type", ["line", "bar", "horizontal_bar", "scatter", "pie", "auto"])
def test_generate_all_chart_types(client, clean_uploads, chart_type):
    xlsx = make_simple_xlsx()
    file_id = _upload(client, clean_uploads, xlsx)
    response = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": chart_type, "format": "png"},
    )
    assert response.status_code == 200
    assert response.json()["chart_base64"]


@pytest.mark.parametrize("theme", ["professional", "eventcore", "minimal", "vibrant", "academic"])
def test_generate_all_themes(client, clean_uploads, theme):
    xlsx = make_simple_xlsx()
    file_id = _upload(client, clean_uploads, xlsx)
    response = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": "bar", "format": "png", "theme": theme},
    )
    assert response.status_code == 200
    assert response.json()["chart_base64"]


def test_generate_missing_file_id_returns_404(client):
    response = client.post(
        "/api/generate",
        json={"file_id": MISSING_FILE_ID, "format": "png"},
    )
    assert response.status_code == 404


def test_generate_with_custom_title_and_labels(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "line",
            "format": "png",
            "title": "Trend Over Time",
            "xlabel": "Period",
            "ylabel": "Value ($)",
        },
    )
    assert response.status_code == 200


def test_generate_with_custom_colors(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "format": "png",
            "colors": ["#FF0000", "#00FF00"],
        },
    )
    assert response.status_code == 200


def test_generate_empty_colors_returns_422(client, uploaded_file_id):
    # field_validator rejects an empty colors list
    response = client.post(
        "/api/generate",
        json={"file_id": uploaded_file_id, "chart_type": "bar", "colors": []},
    )
    assert response.status_code == 422


def test_generate_with_grid_options(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "format": "png",
            "grid": {"enabled": True, "linestyle": "dashed", "alpha": 0.5},
        },
    )
    assert response.status_code == 200


def test_generate_invalid_grid_linestyle_returns_422(client, uploaded_file_id):
    # linestyle must be Literal['solid', 'dashed', 'dotted']
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "grid": {"enabled": True, "linestyle": "wavy"},
        },
    )
    assert response.status_code == 422


def test_generate_with_font_options(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "format": "png",
            "fonts": {"family": "serif", "title_size": 20, "label_size": 14, "tick_size": 10},
        },
    )
    assert response.status_code == 200


def test_generate_with_unit_formatting(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "format": "png",
            "units": {"y_prefix": "$", "y_suffix": ""},
        },
    )
    assert response.status_code == 200


def test_generate_with_data_labels(client, uploaded_file_id):
    response = client.post(
        "/api/generate",
        json={
            "file_id": uploaded_file_id,
            "chart_type": "bar",
            "format": "png",
            "data_labels": {"show": True, "format": ".0f"},
        },
    )
    assert response.status_code == 200


def test_generate_pie_chart(client, clean_uploads):
    xlsx = make_pie_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "pie.xlsx")
    response = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": "pie", "format": "png"},
    )
    assert response.status_code == 200
    assert base64.b64decode(response.json()["chart_base64"])[:8] == PNG_HEADER


def test_generate_scatter_chart(client, clean_uploads):
    xlsx = make_scatter_xlsx()
    file_id = _upload(client, clean_uploads, xlsx, "scatter.xlsx")
    response = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": "scatter", "format": "png"},
    )
    assert response.status_code == 200
    assert base64.b64decode(response.json()["chart_base64"])[:8] == PNG_HEADER
