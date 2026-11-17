---
id: computing-software.qa-testing-engineering.jest-pytest.diff-and-patch-coverage-gates
name: diff-and-patch-coverage-gates
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [diff-coverage, patch-coverage, code-coverage, codecov, diff-cover, coverage-gate, pull-request-checks]
level: practitioner
status: verified
description: "Gate pull requests on coverage of changed lines (diff/patch coverage) with diff-cover or Codecov, instead of absolute project coverage that legacy code drags down."
sources:
  - https://github.com/Bachmann1234/diff_cover
  - https://docs.codecov.com/docs/commit-status
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diff (patch) coverage gates

**Goal:** new and changed code is tested, without blocking PRs on historic coverage debt.

## diff-cover (any Cobertura/LCOV/JaCoCo XML)
```bash
pytest --cov=src --cov-branch --cov-report=xml        # coverage.xml
git fetch origin main
diff-cover coverage.xml --compare-branch=origin/main --fail-under=80 --branch-coverage --format markdown:diff-cover.md
```
`--markdown-report` still exists but is deprecated in diff-cover 10 in favour of `--format markdown:<path>`. Without `--branch-coverage`, only line data is used.
JS: `jest --coverage --coverageReporters=cobertura` writes `coverage/cobertura-coverage.xml` (checked); use that file with the same command. diff-cover also reads Clover, JaCoCo and LCOV reports per its README (JaCoCo not run here).

## Codecov
```yaml
# codecov.yml
coverage:
  status:
    project:
      default: { target: auto, threshold: 1% }   # project may not drop more than 1%
    patch:
      default: { target: 80% }                   # changed lines must be 80% covered
```
Upload with `codecov/codecov-action` (token from secrets; v5 and later exist, see the codecov-upload-and-flags skill). The YAML above passes `https://codecov.io/validate`.

## Practices
- Use branch coverage, not just lines, for the patch.
- Exclude generated code and pure config from coverage (`omit` / `coveragePathIgnorePatterns`).
- A patch gate is a floor, not a goal; review assertions in the tests.

## Gotchas
- diff-cover compares against `--compare-branch` with git, so the base ref must exist locally; in CI fetch it (`git fetch origin main`, as above; a shallow clone is a likely cause when it is missing).
- Moving code counts as changed lines; a refactor PR may need a waiver comment.

## Verify
A PR adding an untested function fails the patch check with the uncovered lines listed. Run locally: a branch adding an untested function gave `src/m.py (50.0%): Missing lines 5-7` and exit code 1.
