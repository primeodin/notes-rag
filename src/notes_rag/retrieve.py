"""Load Markdown notes and retrieve by bag-of-words cosine similarity."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path

TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


@dataclass(frozen=True)
class Note:
    path: Path
    title: str
    body: str

    @property
    def text(self) -> str:
        return f"{self.title}\n{self.body}"


def load_notes(notes_dir: Path) -> list[Note]:
    notes: list[Note] = []
    for path in sorted(notes_dir.glob("**/*.md")):
        raw = path.read_text(encoding="utf-8")
        lines = raw.strip().splitlines()
        title = path.stem.replace("-", " ")
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("#").strip() or title
            body = "\n".join(lines[1:]).strip()
        else:
            body = raw.strip()
        notes.append(Note(path=path, title=title, body=body))
    return notes


def _tf(tokens: list[str]) -> dict[str, float]:
    counts: dict[str, float] = {}
    for t in tokens:
        counts[t] = counts.get(t, 0.0) + 1.0
    n = float(len(tokens) or 1)
    return {k: v / n for k, v in counts.items()}


def _dot(a: dict[str, float], b: dict[str, float]) -> float:
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def _norm(a: dict[str, float]) -> float:
    return math.sqrt(sum(v * v for v in a.values())) or 1.0


def retrieve(notes: list[Note], query: str, k: int = 2) -> list[tuple[Note, float]]:
    if not notes:
        return []
    q = _tf(tokenize(query))
    scored: list[tuple[Note, float]] = []
    for note in notes:
        vec = _tf(tokenize(note.text))
        score = _dot(q, vec) / (_norm(q) * _norm(vec))
        scored.append((note, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(n, s) for n, s in scored[:k] if s > 0]
