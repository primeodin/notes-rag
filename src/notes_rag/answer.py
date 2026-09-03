"""Turn retrieved notes into an answer — mock or OpenAI-compatible."""

from __future__ import annotations

import os
from dataclasses import dataclass

from notes_rag.retrieve import Note


@dataclass
class Answerer:
    mock: bool = False
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls, *, mock: bool = False) -> "Answerer":
        return cls(
            mock=mock,
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        )

    def answer(self, question: str, hits: list[tuple[Note, float]]) -> str:
        if not hits:
            return "I could not find relevant notes. Add Markdown under notes/ and try again."
        cites = ", ".join(n.title for n, _ in hits)
        context = "\n\n".join(f"### {n.title}\n{n.body}" for n, _ in hits)
        if self.mock:
            top = hits[0][0]
            snippet = " ".join(top.body.split())[:180]
            return (
                f"[mock] Based on {cites}: {snippet}"
                f"{'…' if len(top.body) > 180 else ''} "
                f"(question: {question!r})"
            )
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Export a key, or pass --mock to practice offline."
            )
        import json
        import urllib.request

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Answer using ONLY the provided notes. Cite note titles. "
                        "If the notes are insufficient, say you do not know."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Notes:\n{context}\n\nQuestion: {question}",
                },
            ],
            "temperature": 0.2,
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 — user-controlled URL via env
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"].strip()
