# notes-rag

> Day-2 of PrimeOdin’s daily public builds — RAG over a folder of Markdown notes.

**Retrieve → cite → answer.** No vector-DB soup on day one. Bag-of-words cosine keeps the machine small enough to read.

## 60-second start

```bash
git clone https://github.com/primeodin/notes-rag.git
cd notes-rag
pip install -e ".[dev]"
pytest
python -m notes_rag --mock "What is a git remote?"
```

You should see a `[mock]` answer plus a **Sources** list. That means retrieval works before you spend a token.

## Real answers (optional)

```bash
export OPENAI_API_KEY=sk-...
# optional: export OPENAI_BASE_URL=http://localhost:11434/v1
python -m notes_rag "What is RAG?"
```

Drop your own `.md` files in `notes/` and ask again.

## What you just built

| Piece | Job |
| --- | --- |
| `retrieve.py` | Load Markdown, score with bag-of-words cosine |
| `answer.py` | Mock or OpenAI-compatible completion grounded in hits |
| `cli.py` | Question in → answer + citations out |
| `notes/` | Sample teaching notes (git, Ollama, RAG, pytest) |

## Change one thing

1. Add `notes/my-topic.md` and ask a question only that file can answer  
2. Raise `--k` to pull more context  
3. Swap bag-of-words for real embeddings later — keep the same CLI  

## Help / good first issues

Scoped tickets live in [Issues](https://github.com/primeodin/notes-rag/issues). Open contribution ideas:

- **#1** — [`--json` CLI output for answer + sources](https://github.com/primeodin/notes-rag/issues/1)
- **#3** — [`CONTRIBUTING.md` for first-timers](https://github.com/primeodin/notes-rag/issues/3)

New to pull requests? Start at [first-commit-ai](https://github.com/primeodin/first-commit-ai), then come back.

## Daily builds series

Tiny, tested teaching repos — starter → mid. Ship one, read it, then climb:

| Lane | Repo | Why open it |
| --- | --- | --- |
| Starter chat | [first-commit-ai](https://github.com/primeodin/first-commit-ai) | Mock-first chat CLI + pytest |
| Starter RAG (this) | [notes-rag](https://github.com/primeodin/notes-rag) | Retrieve, cite, answer over Markdown notes |
| Starter tokenizer | [tiny-bpe-tokenizer](https://github.com/primeodin/tiny-bpe-tokenizer) | Watch text become token IDs — train, encode, decode |
| Attention mid | [attention-warrior](https://github.com/primeodin/attention-warrior) | Transformer attention you can hold in one hand |
| Shop skills | [mister-jay](https://github.com/primeodin/mister-jay) | Interactive DIY drills (vehicle, electrical, plumbing) — [live](https://primeodin.github.io/mister-jay/) |
| Literacy (Sinhala) | [jay-ai-sinhala](https://github.com/primeodin/jay-ai-sinhala) | Friends 70+ learning GitHub + AI — [live](https://primeodin.github.io/jay-ai-sinhala/) |
| Systems DIY | [camera-selector](https://github.com/primeodin/camera-selector) | NVR/Frigate camera planning — [live](https://primeodin.github.io/camera-selector/) |

Weekday cadence, in order: chat CLI → RAG (this) → tokenizer (shipped) → tool agent → prompt lab → embeddings → vision → memory → shop-skill explainer.

Profile forge: [github.com/primeodin](https://github.com/primeodin)

## License

MIT
