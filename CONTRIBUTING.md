# Contributing to notes-rag

Welcome. This repo is a **day-2 teaching RAG** — retrieve, cite, answer over Markdown. Keep that bar in mind.

## Map (fork → PR)

1. **Fork** this repo on GitHub, then clone your fork:
   ```bash
   git clone https://github.com/<you>/notes-rag.git
   cd notes-rag
   ```
2. **Install** in editable mode with test deps:
   ```bash
   pip install -e ".[dev]"
   ```
3. **Prove the wiring** before you change anything:
   ```bash
   pytest
   python -m notes_rag --mock "What is a git remote?"
   ```
   You want `7 passed` and a `[mock]` answer plus **Sources**. No API key needed.
4. **Branch** for one small change:
   ```bash
   git checkout -b my-first-pr
   ```
5. **Ship** a focused PR back to `primeodin/notes-rag`:
   - one idea per PR
   - include or update a test when behavior changes
   - say what you ran (`pytest`, the mock ask)

## Add a Markdown note

Drop a new `.md` under `notes/`, then ask a question only that file can answer:

```bash
# edit notes/my-topic.md
python -m notes_rag --mock "question only my-topic answers"
```

Keep titles short. Retrieval is bag-of-words cosine — clear headings help more than fancy frontmatter.

## Add or extend a test

Tests live under `tests/`. Prefer a mock/offline case that fails without your change and passes with it. Run `pytest` before you push.

## Good first issues

Scoped tickets (file named in the issue body) live in [Issues](https://github.com/primeodin/notes-rag/issues). After this guide ships, pick whatever is still open — or propose a tiny docs/test PR in a new issue.

Claim one with a comment, ask questions in the thread, then open the PR. Docs count.

## Shop rules

- **Keep it small.** No vector-DB pile-ons, no extra services "while we're here."
- **Mock stays sacred.** Offline tests and `--mock` must keep working without secrets.
- **Teach by running.** Prefer a note, a test, or a one-line CLI flag over a theory dump.
- **Match the voice.** Short, concrete, honest — shop notes, not pitch decks.

## What to skip

Please don't open PRs that:

- add a heavy embedding/vector stack on day one
- require paid APIs in the default path
- rewrite the README for marketing tone
- bundle unrelated refactors with a feature

Questions? Comment on the issue you're claiming — that thread is the right place.
