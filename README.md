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
python -m notes_rag --mock --json "What is a git remote?"  # machine-readable answer + sources
python -m notes_rag --list-notes                          # print indexed note titles + files
```

**Expected stdout** (deterministic on the bundled `notes/` corpus + `--mock` — yours should match):

```text
# pytest
.......                                                                  [100%]
7 passed

# mock ask
[mock] Based on Git remotes, What RAG is: A remote is a shared copy of your repo, usually on GitHub. `git push` sends your commits to the remote. `git pull` brings remote commits into your local branch. Always `git status`… (question: 'What is a git remote?')

Sources:
  - Git remotes (git-remotes.md, score=0.537)
  - What RAG is (rag-idea.md, score=0.241)
```

That `[mock]` answer plus **Sources** means retrieval works before you spend a token. If titles or scores drift, the note corpus or scorer changed — open an issue before "fixing" ranking by eye.

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for fork → install → mock → PR. Scoped tickets live in [Issues](https://github.com/primeodin/notes-rag/issues).

**Open (good first issue):**
- [#7](https://github.com/primeodin/notes-rag/issues/7) — `docs/how-scoring-works.md` (hand-worked bag-of-words cosine)
- [#8](https://github.com/primeodin/notes-rag/issues/8) — `--list-notes` flag (print indexed titles, no question)

**Shipped:**
- `#3` `CONTRIBUTING.md` for first-timers
- `#1` `--json` CLI output — merged from community PR [#6](https://github.com/primeodin/notes-rag/pull/6). Thanks!

New to pull requests? Start at [first-commit-ai](https://github.com/primeodin/first-commit-ai), then come back.

## Daily builds series

Tiny, tested teaching repos — starter → mid. Ship one, read it, then climb:

| Lane | Repo | Why open it |
| --- | --- | --- |
| Starter chat | [first-commit-ai](https://github.com/primeodin/first-commit-ai) | Mock-first chat CLI + pytest |
| Starter RAG (this) | [notes-rag](https://github.com/primeodin/notes-rag) | Retrieve, cite, answer over Markdown notes |
| Starter tokenizer | [tiny-bpe-tokenizer](https://github.com/primeodin/tiny-bpe-tokenizer) | Watch text become token IDs — train, encode, decode |
| Mid tool agent | [tiny-tool-agent](https://github.com/primeodin/tiny-tool-agent) | ReAct: Thought, Action, Observation, Final Answer |
| Attention mid | [attention-warrior](https://github.com/primeodin/attention-warrior) | Transformer attention you can hold in one hand |
| Shop skills | [mister-jay](https://github.com/primeodin/mister-jay) | Interactive DIY drills (vehicle, electrical, plumbing) — [live](https://primeodin.github.io/mister-jay/) |
| Literacy (Sinhala) | [jay-ai-sinhala](https://github.com/primeodin/jay-ai-sinhala) | Friends 70+ learning GitHub + AI — [live](https://primeodin.github.io/jay-ai-sinhala/) |
| Systems DIY | [camera-selector](https://github.com/primeodin/camera-selector) | NVR/Frigate camera planning — [live](https://primeodin.github.io/camera-selector/) |

Weekday cadence, in order: chat CLI → RAG (this) → tokenizer → tool agent (shipped) → prompt lab → embeddings → vision → memory → shop-skill explainer.

Profile forge: [github.com/primeodin](https://github.com/primeodin)

## License

MIT
