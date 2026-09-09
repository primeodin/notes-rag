# How scoring works

The scorer compares token frequencies, not meanings. Here is a tiny example you
can check by hand against [`retrieve.py`](../src/notes_rag/retrieve.py).

## 1. Turn text into tokens

Query: `Git remote?` Two Markdown notes:

```markdown
# Git
git remote
```

```markdown
# Remote
remote remote
```

The title **and** body are scored. Text is lowercased, then `[a-z0-9]+` matches
runs of ASCII letters or digits. Punctuation separates tokens; it is not kept.
The query becomes `[git, remote]`, note A `[git, git, remote]`, and note B
`[remote, remote, remote]`.

## 2. Count and normalize

Term frequency is each token's count divided by the total number of tokens.
Using the coordinate order `(git, remote)`:

| Text | Counts | Term-frequency vector |
| --- | --- | --- |
| Query | `(1, 1)` | `(1/2, 1/2)` |
| A: Git | `(2, 1)` | `(2/3, 1/3)` |
| B: Remote | `(0, 3)` | `(0, 1)` |

Word order does not affect these vectors. Repeating only `remote` still gives
note B a frequency of 1 for that token.

## 3. Compute cosine similarity

Multiply matching coordinates and add them for the dot product. The norm is
the square root of the sum of squared coordinates. Then:

```text
score = dot(query, note) / (norm(query) * norm(note))

norm(query) = sqrt(1/4 + 1/4) = sqrt(2)/2

A: dot = (1/2 * 2/3) + (1/2 * 1/3) = 1/2
   norm = sqrt(4/9 + 1/9) = sqrt(5)/3
   score = (1/2) / (sqrt(2)/2 * sqrt(5)/3) = 3/sqrt(10) = 0.948683...

B: dot = (1/2 * 0) + (1/2 * 1) = 1/2
   norm = sqrt(0 + 1) = 1
   score = (1/2) / (sqrt(2)/2 * 1) = 1/sqrt(2) = 0.707107...
```

## 4. Rank and keep positive hits

Scores are sorted highest first. With `k=2`, A comes before B; the CLI displays
their scores as `0.949` and `0.707`. With `k=1`, only A remains.
The scorer takes the first `k` entries, then keeps only scores greater than 0.
A query such as `pytest` shares no tokens with either note: both dot products
are 0, so neither note is returned, even with `k=2`.

Raising a positive `--k` lets more lower-ranked, positive-score notes into the
answer's context; it does not change their scores or admit zero-score notes.
