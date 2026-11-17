---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-xdist-parallel-runs
name: pytest-xdist-parallel-runs
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, pytest-xdist, parallel-execution, worker-id, loadscope, loadgroup, python]
level: practitioner
status: verified
description: "Run pytest in parallel with pytest-xdist: -n auto, distribution modes, per-worker resources via worker_id, session fixtures across workers and debugging order issues."
sources:
  - https://pytest-xdist.readthedocs.io/en/stable/
  - https://pytest-xdist.readthedocs.io/en/stable/distribution.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel runs with pytest-xdist

**Goal:** cut suite time by running tests across CPU cores (or machines) safely.

## Basics
```bash
pip install pytest-xdist
pytest -n auto                 # one worker per physical core (-n logical: logical cores, needs psutil)
pytest -n 8 --dist loadscope   # keep tests of the same module/class on one worker
pytest -n 4 --dist loadgroup   # honour @pytest.mark.xdist_group("db")
pytest -n 4 --dist worksteal   # rebalance when durations vary a lot
```

## Per-worker isolation
```python
@pytest.fixture(scope="session")
def db_name(worker_id):            # 'gw0', 'gw1', ... or 'master' without xdist
    name = f"test_{worker_id}"
    create_database(name); yield name; drop_database(name)
```
Also: unique ports, temp dirs (`tmp_path_factory` is already per worker), separate test accounts.

## Session fixtures run once per worker
To do something once across all workers (e.g. build assets), use a file lock:
```python
from filelock import FileLock
@pytest.fixture(scope="session")
def built_assets(tmp_path_factory, worker_id):
    root = tmp_path_factory.getbasetemp().parent
    with FileLock(str(root / "assets.lock")):
        marker = root / "assets.done"
        if not marker.exists(): build_assets(); marker.write_text("ok")
```

## Gotchas
- Tests that passed serially failing in parallel = shared state or order dependence (`flakiness-root-causes`).
- `-s` / print debugging is awkward with workers; use `-n 0` to debug. `-p no:xdist` errors with "unrecognized arguments: -n" if `-n` is still passed or set in `addopts`.
- Coverage: pytest-cov supports xdist automatically (`--cov` combines worker data).
- Very fast suites can be slower with xdist (worker start-up); measure.

## Verify
`pytest -n auto` with pytest-randomly installed passes repeatedly with the same results as a serial run.
