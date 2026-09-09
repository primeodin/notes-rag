import json
from pathlib import Path

from notes_rag.answer import Answerer
from notes_rag.cli import main
from notes_rag.retrieve import load_notes, retrieve

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"


def test_loads_sample_notes():
    notes = load_notes(NOTES)
    assert len(notes) >= 4
    titles = {n.title.lower() for n in notes}
    assert any("remote" in t for t in titles)
    assert any("pytest" in t for t in titles)


def test_retrieve_git_remote():
    notes = load_notes(NOTES)
    hits = retrieve(notes, "What is a git remote?", k=2)
    assert hits
    assert "remote" in hits[0][0].title.lower() or "remote" in hits[0][0].body.lower()


def test_retrieve_rag_idea():
    notes = load_notes(NOTES)
    hits = retrieve(notes, "What is retrieval augmented generation?", k=2)
    assert hits
    assert "rag" in hits[0][0].title.lower() or "retrieval" in hits[0][0].body.lower()


def test_retrieve_pytest_basics():
    notes = load_notes(NOTES)
    hits = retrieve(notes, "How do I run pytest?", k=2)
    assert hits
    top = hits[0][0]
    assert "pytest" in top.title.lower() or "pytest" in top.body.lower()


def test_mock_answer_cites(capsys):
    code = main(["--mock", "--notes", str(NOTES), "What is a git remote?"])
    out = capsys.readouterr().out
    assert code == 0
    assert "[mock]" in out
    assert "Sources:" in out


def test_mock_answer_json_output(capsys):
    code = main(["--mock", "--json", "--notes", str(NOTES), "What is a git remote?"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert code == 0
    assert "[mock]" in data["answer"]
    assert data["sources"]
    assert {"title", "file", "score"}.issubset(data["sources"][0])


def test_empty_notes_dir(tmp_path, capsys):
    empty = tmp_path / "empty"
    empty.mkdir()
    code = main(["--mock", "--notes", str(empty), "anything"])
    out = capsys.readouterr().out
    assert code == 0
    assert "could not find" in out.lower()


def test_missing_key_without_mock():
    a = Answerer(mock=False, api_key=None)
    notes = load_notes(NOTES)
    hits = retrieve(notes, "git remote", k=1)
    try:
        a.answer("git remote", hits)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "OPENAI_API_KEY" in str(exc)


def test_list_notes(capsys):
    code = main(["--list-notes", "--notes", str(NOTES)])
    out = capsys.readouterr().out
    assert code == 0
    assert "Git remotes (git-remotes.md)" in out
    assert "What RAG is (rag-idea.md)" in out


def test_list_notes_prefers_list_over_question(capsys):
    code = main(["--list-notes", "--notes", str(NOTES), "What is a git remote?"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Git remotes (git-remotes.md)" in out
    assert "[mock]" not in out


def test_missing_question_without_list_notes(capsys):
    code = main(["--notes", str(NOTES)])
    err = capsys.readouterr().err
    assert code == 2
    assert "the following arguments are required: question" in err


def test_list_notes_missing_dir(tmp_path, capsys):
    missing = tmp_path / "nonexistent"
    code = main(["--list-notes", "--notes", str(missing)])
    err = capsys.readouterr().err
    assert code == 1
    assert "notes folder not found" in err

