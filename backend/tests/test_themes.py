"""
Integration tests for GET /api/themes.
"""

EXPECTED_THEMES = {"professional", "eventcore", "minimal", "vibrant", "academic"}


def test_get_themes_returns_200(client):
    response = client.get("/api/themes")
    assert response.status_code == 200
    body = response.json()
    assert "themes" in body
    assert "default_theme" in body
    assert body["default_theme"] == "professional"
    assert EXPECTED_THEMES == set(body["themes"].keys())


def test_themes_have_required_keys(client):
    response = client.get("/api/themes")
    assert response.status_code == 200
    for name, theme in response.json()["themes"].items():
        assert "colors" in theme, f"Theme '{name}' missing 'colors'"
        assert isinstance(theme["colors"], list), f"Theme '{name}' colors must be a list"
        assert len(theme["colors"]) > 0, f"Theme '{name}' colors must not be empty"
        assert "background" in theme, f"Theme '{name}' missing 'background'"
        assert "font_family" in theme, f"Theme '{name}' missing 'font_family'"
        assert "grid_color" in theme, f"Theme '{name}' missing 'grid_color'"
