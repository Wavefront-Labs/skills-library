---
id: computing-software.software-engineering.python.coverage-measurement-with-coverage-py
name: coverage-measurement-with-coverage-py
category: computing-software
field: software-engineering
product: python
tags: [python, python-testing, coverage-py, branch-coverage, pytest-cov, coverage-reports, ci, py-test-quality]
level: practitioner
status: verified
description: "Measure Python test coverage with coverage.py: branch coverage, config in pyproject, subprocess and parallel combining, exclusions, diff coverage and CI thresholds."
sources:
  - https://coverage.readthedocs.io/en/latest/
  - https://coverage.readthedocs.io/en/latest/branch.html
  - https://coverage.readthedocs.io/en/latest/subprocess.html
  - https://pytest-cov.readthedocs.io/en/latest/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Coverage measurement with coverage.py

**Goal:** an honest coverage number (branches, subprocesses, all source files) enforced in CI without gaming.

## 1. Configure in pyproject.toml
```toml
[tool.coverage.run]
branch = true
source = ["src/mypkg"]          # also reports files never imported (0%)
parallel = true                 # unique data file per process
relative_files = true           # portable paths for CI merges

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 85
exclude_also = [
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@(abc\\.)?abstractmethod",
    "if __name__ == .__main__.:",
]
```

## 2. Run
```bash
coverage run -m pytest
coverage combine          # merge .coverage.* from parallel/subprocess runs
coverage report
coverage html             # htmlcov/index.html, highlights partial branches
coverage xml              # for Codecov/Sonar/GitLab
# or with the plugin
pytest --cov=mypkg --cov-branch --cov-report=term-missing --cov-fail-under=85
```

## 3. Branch coverage
Line coverage counts `if x: y()` as covered when `x` is always true. Branch coverage tracks each possible jump; the report lists `12->15` for a never-taken edge. Mark impossible branches with `# pragma: no branch` sparingly.

## 4. Subprocesses and multiprocessing
Code run in child processes is invisible unless coverage starts there too:
- Set `COVERAGE_PROCESS_START=pyproject.toml` and install the startup hook (coverage 7.10+ (confirmed in the changelog and run on 7.16): `[tool.coverage.run] patch = ["subprocess"]`, which also needs `parallel = true` and a `coverage combine`; older: a `.pth` file calling `coverage.process_startup()`).
- `pytest-cov` handles `multiprocessing` and xdist workers automatically.
- Then `coverage combine`.

## 5. Diff coverage in review
`diff-cover coverage.xml --compare-branch=origin/main --fail-under=90` checks only changed lines: enforces coverage on new code without demanding a legacy cleanup.

## Gotchas
- Without `source`, unimported modules do not appear, inflating the percentage.
- Combining data from different machines needs `relative_files = true` or `[paths]` remapping.
- Coverage proves lines ran, not that assertions checked them; pair with mutation testing (mutmut) on critical modules.
- `fail_under` on a falling legacy number causes "coverage gaming" (trivial tests); prefer diff coverage plus a slowly ratcheted floor.
- Running under coverage slows tests. The `sysmon` core (`[run] core = "sysmon"` or `COVERAGE_CORE=sysmon`) is the default on Python 3.14+; on 3.12/3.13 it does not support branch coverage, so it does not fit this config.

## Verify
- `coverage report` lists every module under `src/`, branch columns are present, and CI fails when `fail_under` is not met.
