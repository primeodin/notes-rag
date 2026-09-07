# Pytest basics

Pytest is the usual way to run tests in Python teaching repos.
You write plain functions whose names start with `test_`, and you check expectations with `assert`.
Run the suite with `pytest` from the project root — no secrets and no network needed for the sample tests here.
Tip: when a test fails, read the assertion diff first; it usually names the exact value that went wrong.
