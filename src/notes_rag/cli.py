"""CLI for notes-rag."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from notes_rag.answer import Answerer
from notes_rag.retrieve import load_notes, retrieve


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="notes-rag",
        description="Ask a question over a folder of Markdown notes (retrieve → cite → answer).",
        epilog=(
            "Examples:\n"
            "  python -m notes_rag --mock \"What is a git remote?\"\n"
            "  python -m notes_rag --notes ./notes --mock \"What is RAG?\"\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("question", help="Your question")
    p.add_argument(
        "--notes",
        type=Path,
        default=Path("notes"),
        help="Folder of .md notes (default: ./notes)",
    )
    p.add_argument("--k", type=int, default=2, help="How many notes to retrieve")
    p.add_argument(
        "--mock",
        action="store_true",
        help="Answer from retrieved notes without calling an API",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print a single JSON object with answer and sources",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    notes_dir = args.notes
    if not notes_dir.is_dir():
        print(f"error: notes folder not found: {notes_dir}", file=sys.stderr)
        return 1
    notes = load_notes(notes_dir)
    hits = retrieve(notes, args.question, k=args.k)
    if not hits:
        print(
            f"no notes matched — try different words or add a note under {notes_dir}",
            file=sys.stderr,
        )
        return 1
    answerer = Answerer.from_env(mock=args.mock)
    try:
        answer = answerer.answer(args.question, hits)
        if args.json:
            sources = [
                {"title": note.title, "file": note.path.name, "score": score}
                for note, score in hits
            ]
            print(json.dumps({"answer": answer, "sources": sources}))
        else:
            print(answer)
            if hits:
                print("\nSources:")
                for note, score in hits:
                    print(f"  - {note.title} ({note.path.name}, score={score:.3f})")
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
