"""
Interview Task: Bookmarks API
==============================
Build a REST API for managing URL bookmarks with tagging and filtering.

Requirements given by interviewer:
1. POST /bookmarks       — create a bookmark (url, title, optional tags)
2. GET  /bookmarks       — list all bookmarks, filterable by tag
3. GET  /bookmarks/{id}  — get a single bookmark
4. DELETE /bookmarks/{id} — delete a bookmark
5. Input validation on URL format
6. Proper HTTP status codes and error responses
"""

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, HttpUrl


# --- Models ---

class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str = Field(min_length=1, max_length=200)
    tags: list[str] = []


class Bookmark(BaseModel):
    id: str
    url: str
    title: str
    tags: list[str]
    created_at: datetime


# --- App & Storage ---

app = FastAPI()

# --- Security Middleware (the Python equivalent of helmet) ---

# CORS — controls which frontends can call your API.
# In production, replace "*" with your actual frontend origin(s).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

# Trusted Hosts — blocks requests with spoofed Host headers (like helmet's hostFilter).
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourapi.com", "localhost"])


# Security headers middleware — equivalent of helmet's default headers.
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"  # modern best practice: rely on CSP instead
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    return response


# In-memory store. In an interview, this is fine — the interviewer
# cares about API design, not database setup.
bookmarks: dict[str, Bookmark] = {}


# --- Routes ---

@app.post("/bookmarks", response_model=Bookmark, status_code=status.HTTP_201_CREATED)
def create_bookmark(data: BookmarkCreate):
    bookmark = Bookmark(
        id=uuid4().hex[:8],
        url=str(data.url),
        title=data.title,
        tags=[t.lower().strip() for t in data.tags],
        created_at=datetime.now(timezone.utc),
    )
    bookmarks[bookmark.id] = bookmark
    return bookmark


@app.get("/bookmarks", response_model=list[Bookmark])
def list_bookmarks(tag: str | None = Query(default=None, description="Filter by tag")):
    results = list(bookmarks.values())
    if tag:
        results = [b for b in results if tag.lower() in b.tags]
    return results


@app.get("/bookmarks/{bookmark_id}", response_model=Bookmark)
def get_bookmark(bookmark_id: str):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmarks[bookmark_id]


@app.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: str):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[bookmark_id]
