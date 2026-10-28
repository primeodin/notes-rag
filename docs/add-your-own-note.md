# Add your own note

The README says "drop your own `.md` in `notes/`". This page makes that concrete:
what heading shape works, and how to prove the retriever picked *your* file.

## 1. Write a note with a clear title

Create `notes/my-topic.md`:

```markdown
# Rune Chanting

Chanting a rune twice binds the ward to the north gate. The chant is spoken
softly; shouting breaks the ward and the gate stays open.
```

Use a real `# Title` heading and words your question will share — the scorer
treats the title and the body as one text (see
[`how-scoring-works.md`](how-scoring-works.md) for the math).

## 2. Ask a question only that note can answer

```bash
python -m notes_rag --mock "how do I bind the ward to the north gate?"
```

`--mock` needs no API key. You should see a **Sources** line naming your title
and file, for example:

```text
Sources:
  - Rune Chanting (my-topic.md, score=0.623)
```

The exact score depends on the words in your note; what matters is that your
title appears in **Sources**. If it does not, see step 3.

## 3. When a vague title wins the wrong note

- A title like **"Notes"** or **"Ideas"** shares common tokens with almost every
  question, so it can outrank the note you meant. Prefer a distinctive title.
- If the wrong note is returned, add the unique words from your question to your
  note (the chant's *north gate*, the *ward*), or make the heading say what the
  note is about.
- Clear headings beat fancy frontmatter here: this scorer reads only
  `[a-z0-9]+` tokens from the title and body, so YAML frontmatter is not parsed
  and adds no signal.

That is the whole trick: shape the title and words so the bag-of-words cosine
points at your file, then confirm it on the **Sources** line.
