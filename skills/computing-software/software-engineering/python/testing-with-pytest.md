---
id: computing-software.software-engineering.python.testing-with-pytest
name: testing-with-pytest
category: computing-software
field: software-engineering
product: python
tags: [python, pytest, fixtures, parametrize, mocking, monkeypatch, conftest, test-isolation, coverage, pytest-xdist, pytest-mock, tdd, unit-testing, pytest-fixtures]
level: practitioner
status: gated
description: "Structure a pytest suite with fixtures, parametrization, and monkeypatch that stays fast, isolated, and doesn't rot into brittle mocks."
sources: ["pytest docs - fixtures, parametrize, monkeypatch", "personal experience maintaining pytest suites"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Testing with pytest — fixtures and parametrization without a brittle suite

**Goal:** a suite that's fast enough to run on every save, isolated enough that one
test's state never leaks into another, and expressive enough that a failure tells you
what broke without reading the test body.

## 1. Fixture scope is the #1 speed/isolation tradeoff
```python
@pytest.fixture(scope="function")   # default: fresh per test, safest
@pytest.fixture(scope="session")    # one DB connection/container for the whole run
```
`session`/`module` scope speeds up expensive setup (spinning up a test DB, Docker
container) but any fixture that mutates shared state (inserts rows, sets globals)
must clean up itself or tests become order-dependent. Pattern for shared-but-clean:
session-scoped container + function-scoped transaction that rolls back:
```python
@pytest.fixture(scope="session")
def db_engine(): ...                       # one container for the run

@pytest.fixture
def db_session(db_engine):
    conn = db_engine.connect()
    trans = conn.begin()
    yield Session(bind=conn)
    trans.rollback()                       # every test starts clean
```
The SQLAlchemy transaction fixture and the Docker container pattern above were not run (gated: unconfirmed, source is paywalled or blocked).

## 2. conftest.py and fixture discovery
Fixtures in `conftest.py` are auto-available to every test in that directory and
below, no import needed — this is convenient and also how fixture name collisions
sneak in across a large suite. `pytest --fixtures` lists every fixture visible at a
given path with its source file; use it before adding a same-named fixture.

## 3. Parametrize instead of copy-pasting test bodies
```python
@pytest.mark.parametrize("input,expected", [(1, 1), (-1, 1), (0, 0)])
def test_abs(input, expected):
    assert abs(input) == expected
```
Stack multiple `parametrize` decorators for a cartesian product. Give `ids=` for
readable failure output on complex inputs. For "same test, many fixtures"
(e.g. every DB backend), parametrize the *fixture* with `params=` and `request.param`,
not the test function.

## 4. Mocking: patch where it's looked up, not where it's defined
```python
# module_a.py: from module_b import helper
# WRONG: mocker.patch("module_b.helper")   — module_a already bound its own reference
# RIGHT: mocker.patch("module_a.helper")
```
This is the single most common pytest-mock mistake. Use `monkeypatch` (built-in) for
env vars, attributes, and `sys.path`; use `pytest-mock`'s `mocker` fixture (auto-undoes
patches, integrates with pytest's fixture teardown) over raw `unittest.mock.patch` as
a decorator, which is easy to forget to stack correctly with multiple patches.

## 5. Flaky and slow test triage
- `pytest --durations=10` after any suite slowdown — shows the 10 slowest tests;
  usually one fixture doing real network/disk I/O that should be mocked.
- `pytest -p no:randomly` (if using `pytest-randomly`) to confirm a failure isn't
  order-dependent before debugging the "real" bug.
- `pytest-xdist` (`-n auto`) parallelizes across processes — but any fixture touching
  a shared resource (one test DB, one port) now races; give each worker its own
  (`tmp_path`, or a DB-per-worker via `worker_id` fixture).
- Time-dependent flakiness: never call `datetime.now()` in code under test without a
  way to inject a clock (`freezegun`, or pass `now: datetime` as a parameter).

## Gotchas
- `tmp_path`/`tmp_path_factory` (built-in) over manual `tempfile` — auto-cleaned,
  unique per test.
- Assertion rewriting only applies to files pytest collects as tests; a helper
  function imported from a non-test module keeps plain `AssertionError` (less detail).
- `@pytest.mark.skip` vs `xfail`: skip for "can't run here," xfail for "known bug,"
  so a fix shows up as an unexpected pass (`XPASS`) instead of silently staying green.

## Verify
- [ ] Full suite runs green twice in a row with `-p no:randomly` disabled and enabled.
- [ ] `pytest --durations=10` has no single test over ~1s unless justified.
- [ ] Every `mocker.patch` target is the import site, verified by temporarily breaking
      the real implementation and confirming the test still passes (would indicate a
      dead patch) — then reverting.
- [ ] No test depends on another test's side effects (run any single test file alone).

Related: computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring

## Checked
- pytest 9.1.1 with pytest-mock 3.17, xdist 3.8, randomly 5.0 on Python 3.14.0: parametrize (including stacked decorators and `ids=`), fixture `params=`/`request.param`; `mocker.patch('module_b.helper')` did NOT affect `module_a` while `mocker.patch('module_a.helper')` did; `monkeypatch`, `tmp_path`; `--durations` listed the slow test; xfail/XPASS reported; a helper in a non-test module gave a bare `AssertionError: plain` without rewritten detail; `--fixtures` lists sources; `-n 2` and `worker_id` worked; `-p no:randomly` gave a stable order. The SQLAlchemy transaction fixture, freezegun and Docker container snippets were not run.
