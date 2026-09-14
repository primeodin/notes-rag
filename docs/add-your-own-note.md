# Add your own note

From the repository root, create `notes/my-topic.md` with this synthetic note:

```markdown
# Zircon marmalade

Zircon marmalade uses staging code ORCHID-731.
```

Use a clear first-line `# Title` and distinctive words in the body. Then ask a
question that only your note can answer:

```bash
python -m notes_rag --mock "What staging code does zircon marmalade use?"
```

The answer should begin with `[mock]`, mention `ORCHID-731`, and include this
source (the numeric score is omitted here):

```text
Sources:
  - Zircon marmalade (my-topic.md, score=...)
```

Check **Sources**, not just a plausible answer. If your title is missing, check
that the file is under `notes/`, ends in `.md`, and shares actual words with the
question. This scorer does not understand synonyms.

A vague heading like `# Notes` plus generic words can overlap the wrong file.
Make the heading and question sharper, then add distinctive facts/tokens to the
body. Merely increasing `--k` can include more irrelevant notes; it does not
make the top match correct. Clear headings beat fancy frontmatter here: the
first heading is the title, and frontmatter is not a special metadata format.
See [how scoring works](how-scoring-works.md) for the cosine math.

Remove the example file when finished if you do not want it in your corpus.
`--mock` proves retrieval and citations offline; it does not verify a real model's
answer quality.
