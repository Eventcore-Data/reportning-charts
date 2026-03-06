"""
Integration tests for POST /api/upload.
"""

from tests.fixtures.excel_factories import (
    make_multi_section_xlsx,
    make_simple_xlsx,
)

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
XLSM_MIME = "application/vnd.ms-excel.sheet.macroEnabled.12"


def test_upload_valid_xlsx_returns_201(client, clean_uploads):
    xlsx = make_simple_xlsx()
    response = client.post(
        "/api/upload",
        files={"file": ("data.xlsx", xlsx, XLSX_MIME)},
    )
    assert response.status_code == 201
    body = response.json()
    assert "file_id" in body
    assert body["filename"] == "data.xlsx"
    assert body["message"] == "File uploaded successfully"
    preview = body["data_preview"]
    assert preview["columns"] == ["Month", "Revenue"]
    assert preview["total_rows"] == 3
    assert body["sections"] == []


def test_upload_title_row_extracted(client, clean_uploads):
    xlsx = make_simple_xlsx(title="Revenue Report")
    response = client.post(
        "/api/upload",
        files={"file": ("titled.xlsx", xlsx, XLSX_MIME)},
    )
    assert response.status_code == 201
    assert response.json()["extracted_title"] == "Revenue Report"


def test_upload_xlsm_extension_accepted(client, clean_uploads):
    xlsx = make_simple_xlsx()
    response = client.post(
        "/api/upload",
        files={"file": ("macro.xlsm", xlsx, XLSM_MIME)},
    )
    assert response.status_code == 201
    assert "file_id" in response.json()


def test_upload_wrong_extension_returns_400(client, clean_uploads):
    response = client.post(
        "/api/upload",
        files={"file": ("data.csv", b"a,b\n1,2", "text/csv")},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_txt_extension_returns_400(client, clean_uploads):
    response = client.post(
        "/api/upload",
        files={"file": ("data.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


def test_upload_no_file_returns_422(client, clean_uploads):
    response = client.post("/api/upload")
    assert response.status_code == 422


def test_upload_corrupted_xlsx_returns_400(client, clean_uploads):
    response = client.post(
        "/api/upload",
        files={"file": ("bad.xlsx", b"this is not a valid xlsx file", XLSX_MIME)},
    )
    assert response.status_code == 400
    assert "Failed to read Excel file" in response.json()["detail"]


def test_upload_multi_section_returns_sections(client, clean_uploads):
    xlsx = make_multi_section_xlsx()
    response = client.post(
        "/api/upload",
        files={"file": ("multi.xlsx", xlsx, XLSX_MIME)},
    )
    assert response.status_code == 201
    body = response.json()
    sections = body["sections"]
    assert len(sections) == 2
    assert sections[0]["title"] == "Q1 Results"
    assert sections[1]["title"] == "Q2 Results"
    assert sections[0]["index"] == 0
    assert sections[1]["index"] == 1
    assert sections[0]["row_count"] == 3
    assert len(sections[0]["columns"]) > 0


def test_upload_file_persisted_on_disk(client, clean_uploads):
    xlsx = make_simple_xlsx()
    response = client.post(
        "/api/upload",
        files={"file": ("persist.xlsx", xlsx, XLSX_MIME)},
    )
    assert response.status_code == 201
    file_id = response.json()["file_id"]
    upload_path = clean_uploads / "uploads" / f"{file_id}.xlsx"
    assert upload_path.exists()
