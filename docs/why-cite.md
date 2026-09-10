# Why cite (trust the Sources line)

The answer text can sound confident while the wrong note is on top. Citations are the shop light that shows which folders the machine actually opened.

This walkthrough uses the bundled `notes/` corpus and `--mock` — your numbers should match.

## Hand-worked trap: “What is pytest?”

```bash
python -m notes_rag --mock "What is pytest?"
```

**What you get (deterministic on this corpus):**

```text
[mock] Based on What RAG is, Pytest basics: Retrieval-Augmented Generation finds
relevant notes first, then asks a model to answer using those notes. Cite the
note titles you used so the reader can check your work. If nothin…
(question: 'What is pytest?')

Sources:
  - What RAG is (rag-idea.md, score=0.234)
  - Pytest basics (pytest-basics.md, score=0.207)
```

Shop check:

| Line | What it means |
| --- | --- |
| `#1` What RAG is @ `0.234` | Bag-of-words put the wrong folder on the bench first (shared filler words beat the topic title this round) |
| `#2` Pytest basics @ `0.207` | The note that actually answers the question is **second** |
| Mock body | Snippet comes from the **top** hit (`answer.py`), so the prose starts mid-RAG lecture |
| `Based on A, B` | Title list is honest even when ranking is noisy — that is the point of citing |

If you only read the first sentence of the answer, you “learn” RAG while asking about pytest. If you read **Sources**, you see the miss and open `pytest-basics.md` yourself.

## Healthy contrast: “What is a git remote?”

```bash
python -m notes_rag --mock "What is a git remote?"
```

```text
Sources:
  - Git remotes (git-remotes.md, score=0.537)
  - What RAG is (rag-idea.md, score=0.241)
```

Top hit matches the question; the second note still tags along on shared words (`notes`, short tokens). Citation still earns its keep: you can ignore the low-score hitchhiker.

## Empty shelf

```bash
python -m notes_rag --mock "zzzz nonexistent jargon xyzzy"
```

```text
I could not find relevant notes. Add Markdown under notes/ and try again.
```

No Sources block. No fake citations. When overlap is zero, the machine should refuse — not invent a bookshelf.

## Shop judgment

| Do | Don't |
| --- | --- |
| Read **Sources** (title, file, score) before trusting prose | Treat a fluent mock/live paragraph as proof of retrieval |
| Prefer a high-score on-topic hit; treat near-ties as a smell | Assume rank `#1` is always the answer note |
| Keep citations in the CLI / JSON (`--json` → `sources`) | Strip Sources to make demos “cleaner” |
| Fix the corpus or scorer when the wrong note wins often | Yell at the model first — ranking failed before generation |

Live mode still gets the same hit list; the model is told to use only those notes and cite titles. Citations are the gate. Generation never gets to hide which folders were opened.

## See also

- [`how-scoring-works.md`](how-scoring-works.md) — bag-of-words cosine with tiny numbers
- Open tickets: [#11 add-your-own-note](https://github.com/primeodin/notes-rag/issues/11), [#12 empty-hits notice](https://github.com/primeodin/notes-rag/issues/12)
