---
id: computing-software.qa-testing-engineering.jest-pytest.combining-parallel-coverage
name: combining-parallel-coverage
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [coverage-combine, parallel-coverage, subprocess-coverage, nyc-merge, coverage-py]
level: practitioner
status: verified
description: "Combine coverage from parallel workers, subprocesses and CI shards: coverage.py parallel mode and combine, pytest-cov with xdist, nyc merge and istanbul report merging."
sources:
  - https://coverage.readthedocs.io/en/latest/cmd.html#cmd-combine
  - https://coverage.readthedocs.io/en/latest/subprocess.html
  - https://pytest-cov.readthedocs.io/en/latest/xdist.html
  - https://github.com/istanbuljs/nyc#merge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combining coverage from parallel and subprocess runs

## coverage.py
```toml
[tool.coverage.run]
branch = true
parallel = true                 # data files get a machine.pid.random suffix
source = ["src"]
[tool.coverage.paths]
source = ["src/", "/app/src/", "*/site-packages/myapp/"]   # map paths from containers/venvs to one
```
```bash
coverage run -m pytest ...       # each process writes .coverage.<suffix>
coverage combine                 # merges into .coverage (uses [paths] remapping)
coverage report --fail-under=85
coverage xml
```

## Subprocesses
Python child processes are not measured by default. Since coverage 7.10: `[tool.coverage.run] patch = ["subprocess"]`. Older: set `COVERAGE_PROCESS_START=pyproject.toml` and install a `.pth` file that calls `coverage.process_startup()`.

## pytest-cov with xdist
`pytest -n auto --cov=src --cov-report=xml` handles worker data and combining automatically. Don't also run `coverage combine` on top.

## CI shards
```yaml
# each shard
- run: coverage run -m pytest --shard-id=${{ matrix.shard }} --num-shards=4   # with pytest-shard
- uses: actions/upload-artifact@v4
  with: { name: cov-${{ matrix.shard }}, path: .coverage.*, include-hidden-files: true }
# final job
- uses: actions/download-artifact@v4
  with: { pattern: cov-*, merge-multiple: true }
- run: coverage combine && coverage report --fail-under=85
```

## JavaScript (istanbul/nyc)
Each run writes JSON to `.nyc_output/` (or `coverage/coverage-final.json`). Merge:
```bash
npx nyc merge shard-outputs/ merged/coverage.json
npx nyc report --temp-dir merged --reporter=lcov --reporter=text-summary
```
Jest: `--shard=i/n --coverage` per job, then merge `coverage-final.json` files with `istanbul-lib-coverage` or nyc.

## Gotchas
- Hidden files (`.coverage.*`) are skipped by upload-artifact v4 unless `include-hidden-files: true`.
- Mismatched source paths between shards produce duplicate files in the report: fix with `[paths]`.

## Verify
Combined total ≥ every individual shard's total, and the file list has no duplicated paths.
