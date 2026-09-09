# How scoring works (bag-of-words cosine)

This is the exact path `retrieve.py` takes — tiny numbers, no vector DB, no embeddings. If your hand calc disagrees with the code, one of us has a bug.

## The toys

**Query:** `rag notes`

**Three short notes** (title + body, same join the code uses):

| Note | Text scored |
| --- | --- |
| A | `RAG idea` + `Retrieve notes with rag.` |
| B | `Git remotes` + `Notes about remotes.` |
| C | `Pytest basics` + `Write tests with pytest.` |

## 1. Tokenize

Lowercase, keep only `[a-z0-9]+` runs (see `TOKEN` in `retrieve.py`). Punctuation and spaces drop out.

| Source | Tokens |
| --- | --- |
| Query | `rag`, `notes` |
| Note A | `rag`, `idea`, `retrieve`, `notes`, `with`, `rag` |
| Note B | `git`, `remotes`, `notes`, `about`, `remotes` |
| Note C | `pytest`, `basics`, `write`, `tests`, `with`, `pytest` |

## 2. Term-frequency vectors

Each token’s weight = count / length (raw TF, not IDF).

**Query** (length 2): `rag=0.5`, `notes=0.5`

**Note A** (length 6): `rag=2/6=1/3`, `idea=1/6`, `retrieve=1/6`, `notes=1/6`, `with=1/6`

**Note B** (length 5): `git=0.2`, `remotes=0.4`, `notes=0.2`, `about=0.2`

**Note C** (length 6): `pytest=1/3`, `basics=1/6`, `write=1/6`, `tests=1/6`, `with=1/6`

## 3. Dot product, norms, cosine

```
cosine(q, n) = dot(q, n) / (‖q‖ × ‖n‖)
```

‖v‖ is the Euclidean norm of the TF weights. Missing keys count as `0`.

| Pair | Shared mass (dot) | ‖query‖ | ‖note‖ | Cosine |
| --- | --- | --- | --- | --- |
| Query · A | `0.5×(1/3) + 0.5×(1/6) = 0.25` | `√0.5 ≈ 0.707` | `√(2/9) ≈ 0.471` | **0.75** |
| Query · B | `0.5×0.2 = 0.1` | `√0.5 ≈ 0.707` | `√0.28 ≈ 0.529` | **≈ 0.267** |
| Query · C | `0` (no shared tokens) | `√0.5` | `√(2/9)` | **0.0** |

Shop check: A wins because `rag` shows up twice and `notes` once. B only shares `notes`. C shares nothing useful with this query — cosine is exactly zero.

## 4. Rank + the `score > 0` cutoff

`retrieve(..., k=2)` sorts high→low, keeps the top `k`, then **drops any score that is not > 0**.

For this toy set with `--k 2`:

1. Note A — `0.75` → kept  
2. Note B — `≈0.267` → kept  
3. Note C — `0.0` → never returned (cutoff), even if `k` were larger  

## What changes if you raise `--k`?

You ask for a longer shortlist of positive-overlap notes. Zero-score notes still stay out — raising `k` never resurrects a note that shares no tokens with the query.

