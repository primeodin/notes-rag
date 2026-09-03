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
| `notes/` | Sample teaching notes (git, Ollama, RAG) |

## Change one thing

1. Add `notes/my-topic.md` and ask a question only that file can answer  
2. Raise `--k` to pull more context  
3. Swap bag-of-words for real embeddings later — keep the same CLI  

## Daily builds series

| Repo | Level |
| --- | --- |
| [first-commit-ai](https://github.com/primeodin/first-commit-ai) | starter chat CLI |
| **notes-rag** (this) | starter RAG |
| [tiny-bpe-tokenizer](https://github.com/primeodin/tiny-bpe-tokenizer) | starter tokenizer (building in the open) |
| next: tiny tool-calling agent (ReAct, no framework soup) | mid |

Profile: [github.com/primeodin](https://github.com/primeodin)

## License

MIT
