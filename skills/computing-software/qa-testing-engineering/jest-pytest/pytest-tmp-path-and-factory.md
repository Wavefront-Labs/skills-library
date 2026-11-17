---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-tmp-path-and-factory
name: pytest-tmp-path-and-factory
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [tmp-path-factory, tmp-path, tmpdir, basetemp, temporary-files]
level: practitioner
status: verified
description: "Use pytest tmp_path and tmp_path_factory for isolated temp files and dirs, share session-scoped data dirs, control basetemp and retention, and avoid tmpdir legacy."
sources:
  - https://docs.pytest.org/en/stable/how-to/tmp_path.html
  - https://docs.pytest.org/en/stable/reference/reference.html#tmp-path-factory-factory-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tmp_path and tmp_path_factory

## tmp_path (function scope)
```python
def test_writes_report(tmp_path):
    out = tmp_path / "report.csv"
    write_report(out)
    assert out.read_text().splitlines()[0] == "id,total"
```
`tmp_path` is a unique `pathlib.Path` per test under the base temp dir.

## tmp_path_factory (session scope)
```python
@pytest.fixture(scope="session")
def dataset_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("dataset")   # numbered: dataset0, dataset1...
    build_large_fixture(d)
    return d
```
Use to build expensive shared input once; tests should treat it as read-only (copy into `tmp_path` before mutating).

With xdist, session fixtures run once **per worker**; for a truly shared one, lock with `filelock` in `tmp_path_factory.getbasetemp().parent`.

## Location and retention
- Default base: system temp `pytest-of-<user>/pytest-<N>/`; the last 3 runs are kept.
- `--basetemp=build/tmp` sets a fixed dir (wiped at the start of each run): handy for CI artifact upload.
- `tmp_path_retention_count` and `tmp_path_retention_policy` (`all`, `failed`, `none`) in ini options control cleanup.

## Legacy
`tmpdir` / `tmpdir_factory` return `py.path.local`; prefer `tmp_path` in new code.

## Gotchas
- Don't `chdir` into tmp_path without `monkeypatch.chdir` (no automatic restore).
- `--basetemp` pointing at a directory with real files deletes them.
- Windows path length limits: long test names produce long dirs; keep names reasonable.

## Verify
Running with `--basetemp=build/tmp -p no:cacheprovider` leaves per-test dirs you can inspect after a failure.
