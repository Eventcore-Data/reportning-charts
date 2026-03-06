"""
End-to-end integration tests that exercise multi-step workflows.
"""

import base64

from tests.fixtures.excel_factories import make_multi_section_xlsx, make_simple_xlsx

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
PDF_HEADER = b"%PDF"


def test_full_happy_path_flow(client, clean_uploads):
    """Upload → chart-data → generate → download → cleanup → all subsequent calls 404."""
    # 1. Upload
    xlsx = make_simple_xlsx(title="Sales Report")
    up_resp = client.post(
        "/api/upload",
        files={"file": ("sales.xlsx", xlsx, XLSX_MIME)},
    )
    assert up_resp.status_code == 201
    file_id = up_resp.json()["file_id"]

    # 2. Chart data (Plotly)
    cd_resp = client.post(
        "/api/chart-data",
        json={"file_id": file_id, "chart_type": "bar"},
    )
    assert cd_resp.status_code == 200
    assert len(cd_resp.json()["traces"]) > 0

    # 3. Generate (base64 PNG)
    gen_resp = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": "bar", "format": "png"},
    )
    assert gen_resp.status_code == 200
    decoded = base64.b64decode(gen_resp.json()["chart_base64"])
    assert decoded[:8] == PNG_HEADER

    # 4. Download (binary stream)
    dl_resp = client.get(f"/api/chart/{file_id}?format=png")
    assert dl_resp.status_code == 200
    assert dl_resp.content[:8] == PNG_HEADER

    # 5. Cleanup
    cl_resp = client.delete(f"/api/cleanup/{file_id}")
    assert cl_resp.status_code == 200

    # 6. All subsequent calls return 404
    assert client.post("/api/chart-data", json={"file_id": file_id}).status_code == 404
    assert client.post("/api/generate", json={"file_id": file_id}).status_code == 404
    assert client.get(f"/api/chart/{file_id}").status_code == 404
    assert client.delete(f"/api/cleanup/{file_id}").status_code == 404


def test_multi_section_full_flow(client, clean_uploads):
    """Upload a multi-section file; chart-data works independently for each section."""
    xlsx = make_multi_section_xlsx()
    up_resp = client.post(
        "/api/upload",
        files={"file": ("multi.xlsx", xlsx, XLSX_MIME)},
    )
    assert up_resp.status_code == 201
    file_id = up_resp.json()["file_id"]
    sections = up_resp.json()["sections"]
    assert len(sections) == 2

    for i in range(2):
        cd_resp = client.post(
            "/api/chart-data",
            json={"file_id": file_id, "chart_type": "bar", "section_index": i},
        )
        assert cd_resp.status_code == 200, f"section_index={i} failed"
        assert len(cd_resp.json()["traces"]) > 0


def test_all_formats_pipeline(client, clean_uploads):
    """Single upload; generate and verify binary signatures for all three formats."""
    xlsx = make_simple_xlsx()
    file_id = client.post(
        "/api/upload",
        files={"file": ("t.xlsx", xlsx, XLSX_MIME)},
    ).json()["file_id"]

    for fmt, expected_start in [("png", PNG_HEADER), ("pdf", PDF_HEADER)]:
        gen_resp = client.post(
            "/api/generate",
            json={"file_id": file_id, "chart_type": "bar", "format": fmt},
        )
        assert gen_resp.status_code == 200, f"format={fmt} failed"
        decoded = base64.b64decode(gen_resp.json()["chart_base64"])
        assert decoded[: len(expected_start)] == expected_start, f"{fmt} magic bytes wrong"

    # SVG — check for XML content
    svg_resp = client.post(
        "/api/generate",
        json={"file_id": file_id, "chart_type": "bar", "format": "svg"},
    )
    assert svg_resp.status_code == 200
    assert b"<svg" in base64.b64decode(svg_resp.json()["chart_base64"])
