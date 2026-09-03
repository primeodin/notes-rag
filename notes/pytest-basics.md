# Pytest basics

Pytest is a tool that runs your test files and tells you what passed or failed.
A test is a small function whose name starts with `test_`.
Inside a test, `assert` checks that something is true; if it is false, the test fails.
Run all your tests by typing `pytest` in the terminal.
Install pytest first with `pip install pytest`.
If your code crashes before a check even runs, pytest calls that an error, not a fail.
