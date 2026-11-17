---
id: computing-software.software-engineering.python.pytest-builtin-fixtures
name: pytest-builtin-fixtures
category: computing-software
field: software-engineering
product: python
tags: [python, pytest, tmp-path, caplog, capsys, recwarn, request-fixture]
level: practitioner
status: verified
description: "Use pytest's built-in fixtures well: tmp_path for files, capsys/capfd for output, caplog for log assertions, monkeypatch for env, recwarn and request for introspection."
sources: ["https://docs.pytest.org/en/stable/reference/fixtures.html#built-in-fixtures", "https://docs.pytest.org/en/stable/how-to/tmp_path.html", "https://docs.pytest.org/en/stable/how-to/logging.html", "https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest built-in fixtures

**Goal:** test file I/O, console output, logging and warnings without hand-rolled
setup/teardown.

## tmp_path / tmp_path_factory
```python
def test_writes_report(tmp_path):
    out = tmp_path / "report.csv"
    write_report(out, rows)
    assert out.read_text().splitlines()[0] == "id,total"

@pytest.fixture(scope="session")
def sample_repo(tmp_path_factory):
    d = tmp_path_factory.mktemp("repo")      # session-scoped temp dir
    build_fixture_repo(d); return d
```
Unique per test, `pathlib.Path`, kept for the last 3 runs (`--basetemp` to choose location)
for post-mortem. Prefer over `tmpdir` (legacy py.path).

## capsys / capfd
```python
def test_cli_prints_version(capsys):
    main(["--version"])
    out, err = capsys.readouterr()
    assert out.strip() == "mytool 1.4.2"
```
`capfd` captures at file-descriptor level - needed for output from C extensions or
subprocesses inheriting stdout. `capsys.disabled()` context to print through during debugging.

## caplog
```python
import logging
def test_warns_on_retry(caplog):
    caplog.set_level(logging.WARNING, logger="myapp.http")
    call_with_retry()
    assert "retrying" in caplog.text
    assert [r.levelno for r in caplog.records] == [logging.WARNING]
```
If assertions see nothing: the logger has `propagate=False` or a higher level set by your
app's logging config; `caplog` hooks into the root logger.

## monkeypatch
```python
def test_reads_env(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_REGION", "eu-west-1")
    monkeypatch.delenv("APP_DEBUG", raising=False)
    monkeypatch.setattr("myapp.clock.now", lambda: FIXED)
    monkeypatch.chdir(tmp_path)
```
Everything undone after the test. Patch where the name is looked up (`myapp.clock.now`),
not where it was defined.

## Warnings and introspection
```python
def test_deprecated():
    with pytest.warns(DeprecationWarning, match="use load_v2"):
        load()
def test_named(request):
    request.node.name; request.config.getoption("--runslow")
    request.addfinalizer(cleanup)
```
`recwarn` records all warnings; set `filterwarnings = ["error"]` in config to make unexpected
warnings fail the suite.

## Verify
- [ ] No test writes to the repo working tree or real home directory (run suite twice; `git status` clean).
- [ ] `-W error` / `filterwarnings = error` enabled, with explicit ignores for third-party noise.
