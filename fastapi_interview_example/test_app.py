"""Tests for the Bookmarks API — demonstrates interview-quality testing."""

import pytest
from fastapi.testclient import TestClient

from app import app, bookmarks


@pytest.fixture(autouse=True)
def clear_store():
    """Reset in-memory store between tests."""
    bookmarks.clear()
    yield
    bookmarks.clear()


client = TestClient(app)

SAMPLE = {"url": "https://example.com", "title": "Example", "tags": ["dev", "python"]}


# --- Happy paths ---

def test_create_bookmark():
    resp = client.post("/bookmarks", json=SAMPLE)
    assert resp.status_code == 201
    body = resp.json()
    assert body["url"] == "https://example.com/"
    assert body["title"] == "Example"
    assert body["tags"] == ["dev", "python"]
    assert "id" in body
    assert "created_at" in body


def test_list_bookmarks():
    client.post("/bookmarks", json=SAMPLE)
    client.post("/bookmarks", json={"url": "https://other.com", "title": "Other"})
    resp = client.get("/bookmarks")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_by_tag():
    client.post("/bookmarks", json=SAMPLE)
    client.post("/bookmarks", json={"url": "https://other.com", "title": "Other"})

    resp = client.get("/bookmarks", params={"tag": "python"})
    results = resp.json()
    assert len(results) == 1
    assert results[0]["title"] == "Example"


def test_get_single_bookmark():
    created = client.post("/bookmarks", json=SAMPLE).json()
    resp = client.get(f"/bookmarks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Example"


def test_delete_bookmark():
    created = client.post("/bookmarks", json=SAMPLE).json()
    resp = client.delete(f"/bookmarks/{created['id']}")
    assert resp.status_code == 204

    resp = client.get(f"/bookmarks/{created['id']}")
    assert resp.status_code == 404


# --- Error cases ---

def test_get_nonexistent_returns_404():
    resp = client.get("/bookmarks/nope")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Bookmark not found"


def test_delete_nonexistent_returns_404():
    resp = client.delete("/bookmarks/nope")
    assert resp.status_code == 404


def test_invalid_url_returns_422():
    resp = client.post("/bookmarks", json={"url": "not-a-url", "title": "Bad"})
    assert resp.status_code == 422


def test_empty_title_returns_422():
    resp = client.post("/bookmarks", json={"url": "https://example.com", "title": ""})
    assert resp.status_code == 422


def test_missing_required_fields_returns_422():
    resp = client.post("/bookmarks", json={})
    assert resp.status_code == 422
