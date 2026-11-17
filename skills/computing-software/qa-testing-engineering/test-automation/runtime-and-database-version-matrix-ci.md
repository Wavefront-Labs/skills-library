---
id: computing-software.qa-testing-engineering.test-automation.runtime-and-database-version-matrix-ci
name: runtime-and-database-version-matrix-ci
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [ci-version-matrix, compatibility-testing, github-actions, nox]
level: practitioner
status: docs-checked
description: "Run tests against every supported runtime and database version in CI with GitHub Actions matrix, include, exclude, fail-fast and nox sessions."
sources:
  - https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations
  - https://nox.thea.codes/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime and database version compatibility matrix in CI

**Goal:** every version combination the support policy promises is exercised on every change, at a sensible cost.

## GitHub Actions matrix
A matrix strategy lets one job definition create multiple job runs from combinations of variables, for example several language versions or operating systems. Define it with `jobs.<job_id>.strategy.matrix`: one or more variables, each followed by an array of values. Reference values as `${{ matrix.version }}`.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        runtime: ['3.10', '3.11', '3.12', '3.13']
        db: ['13', '17']
        include:
          - runtime: '3.12'
            db: '15'
```
- `include` (a list of objects) expands existing combinations or adds new ones. An include entry is added to original combinations only where it does not overwrite an original value; an entry that cannot be added without overwriting becomes an additional combination.
- `exclude` removes specific configurations; a partial match removes every combination that matches it.
- Matrix values can come from an earlier job via `fromJSON(needs.<job>.outputs.<name>)`.
- `strategy.fail-fast` and `continue-on-error` control failures. The docs state that when any job with `continue-on-error: false` fails, all in-progress and queued jobs are cancelled (fail-fast true), while a failing `continue-on-error: true` job does not affect the others. Set `fail-fast: false` so one red cell does not hide the pattern across the other cells.
- `strategy.max-parallel` caps the jobs that run simultaneously.
- Mark an experimental cell (for example a prerelease runtime) with `continue-on-error: ${{ matrix.experimental }}` to see breakage early without failing the run.

How to start the database for each cell (service containers, container images) is not covered by the cited pages; use the GitHub Actions service container documentation.

## Locally with nox
Nox is a command-line tool that automates testing in multiple Python environments, similar to tox; unlike tox it is configured with a standard Python file. For each session it creates an isolated environment with the right interpreter, installs the dependencies and runs the commands in order.
```python
import nox

@nox.session
def tests(session):
    session.install('pytest')
    session.run('pytest')
```
See the Nox "Configuration and API" page for parametrising sessions over Python versions.

## Gotchas
- Test the oldest and newest of each axis fully; use `include` or a reduced set for the middle versions to control cost.
- Keep the support-policy table and the matrix in step.

## Verify
The support policy table and the matrix list the same versions, and a deliberately version-specific failure shows up in only that cell.

## Checked
2026-11-09: checked against the GitHub Actions matrix page (matrix definition, include and exclude semantics, fromJSON, fail-fast, continue-on-error, max-parallel; the cited URL moved, so the source is the current page) and the Nox home page. Removed because those pages do not state them: the `services:` Postgres container block and health options, `actions/setup-python`, the `nox.session(python=[...])` argument and `nox -s` invocation, tox `envlist` syntax, `uv pip install --resolution lowest-direct`, and the branch-protection check-name claim. Tags `tox` and `database-versions` trimmed.

Method: documentation only; no commands were run.
