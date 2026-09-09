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
            "  python -m notes_rag --list-notes\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("question", nargs="?", default=None, help="Your question")
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
    p.add_argument(
        "--list-notes",
        action="store_true",
        help="Print indexed note titles and filenames, then exit (prefers list mode if question is also passed)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    notes_dir = args.notes
    if not notes_dir.is_dir():
        print(f"error: notes folder not found: {notes_dir}", file=sys.stderr)
        return 1

    if args.list_notes:
        notes = load_notes(notes_dir)
        for note in notes:
            print(f"{note.title} ({note.path.name})")
        return 0

    if not args.question:
        parser.print_usage(file=sys.stderr)
        print("notes-rag: error: the following arguments are required: question", file=sys.stderr)
        return 2

    notes = load_notes(notes_dir)
    hits = retrieve(notes, args.question, k=args.k)
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
