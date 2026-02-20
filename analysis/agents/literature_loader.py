"""
Literature loader — reads HTML and Markdown source files,
extracts clean text, and chunks them for LLM processing.
"""

import os, re
from bs4 import BeautifulSoup
from . import config


def load_file(source_id: str) -> dict | None:
    """Load a single literature file by its source ID (e.g. '#01').
    Returns dict with keys: id, label, type, text, char_count.
    Returns None for PDF files (not machine-readable)."""
    meta = config.LITERATURE_FILES.get(source_id)
    if not meta:
        return None
    if meta["type"] == "pdf":
        return {"id": source_id, "label": meta["label"], "type": "pdf",
                "text": None, "char_count": 0,
                "note": "PDF — requires manual extraction"}

    filepath = os.path.join(config.LIT_DIR, meta["file"])
    if not os.path.exists(filepath):
        return {"id": source_id, "label": meta["label"], "type": meta["type"],
                "text": None, "char_count": 0,
                "note": f"File not found: {meta['file']}"}

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    if meta["type"] == "html":
        text = _extract_html(raw)
    else:  # md
        text = _clean_markdown(raw)

    return {"id": source_id, "label": meta["label"], "type": meta["type"],
            "text": text, "char_count": len(text)}


def load_sources(source_ids: list[str]) -> list[dict]:
    """Load multiple sources. Skips PDFs and missing files."""
    results = []
    for sid in source_ids:
        doc = load_file(sid)
        if doc and doc["text"]:
            results.append(doc)
    return results


def load_all_readable() -> list[dict]:
    """Load all non-PDF literature files."""
    return load_sources([sid for sid, meta in config.LITERATURE_FILES.items()
                         if meta["type"] != "pdf"])


def chunk_text(text: str, max_chars: int = None) -> list[str]:
    """Split text into chunks respecting paragraph boundaries."""
    max_chars = max_chars or config.MAX_CHUNK_CHARS
    if len(text) <= max_chars:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para) + 2  # account for \n\n
        if current_len + para_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def prepare_source_context(sources: list[dict],
                           max_total_chars: int = 500_000) -> str:
    """Combine multiple sources into a single context string with headers.
    Truncates individual sources if total would exceed budget."""
    parts = []
    total = 0
    per_source_budget = max_total_chars // max(len(sources), 1)

    for doc in sources:
        text = doc["text"]
        if len(text) > per_source_budget:
            text = text[:per_source_budget] + "\n\n[... TRUNCATED ...]"
        header = f"═══ SOURCE {doc['id']}: {doc['label']} ═══"
        part = f"{header}\n\n{text}"
        total += len(part)
        if total > max_total_chars:
            break
        parts.append(part)

    return "\n\n" + "\n\n".join(parts) + "\n\n"


# ── Internal helpers ─────────────────────────────────────────────────────────

def _extract_html(html: str) -> str:
    """Extract clean text from HTML, preserving section structure."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, nav, footer elements
    for tag in soup.find_all(["script", "style", "nav", "footer", "header",
                               "aside", "noscript", "iframe"]):
        tag.decompose()

    # Extract text with minimal structure preservation
    lines = []
    for elem in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6",
                                "p", "li", "td", "th", "blockquote",
                                "figcaption", "dt", "dd"]):
        text = elem.get_text(separator=" ", strip=True)
        if not text or len(text) < 3:
            continue
        tag_name = elem.name
        if tag_name in ("h1", "h2"):
            lines.append(f"\n## {text}\n")
        elif tag_name in ("h3", "h4", "h5", "h6"):
            lines.append(f"\n### {text}\n")
        elif tag_name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    result = "\n".join(lines)
    # Collapse excessive whitespace
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def _clean_markdown(md: str) -> str:
    """Clean markdown text — normalize whitespace, remove HTML artifacts."""
    # Remove inline HTML tags that sometimes appear in MD files
    md = re.sub(r"</?[a-zA-Z][^>]*>", "", md)
    # Collapse excessive whitespace
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()
