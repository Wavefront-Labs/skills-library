---
id: computing-software.devops-ci-cd.github-actions.matrix-job-names-and-required-checks
name: matrix-job-names-and-required-checks
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, matrix-job-names, matrix-required-checks, job-name-expression, check-run-name, aggregate-job, ci-ok-job, needs-all-legs, alls-green, if-always-needs, required-status-checks, matrix, matrix-build, branch-protection]
level: practitioner
status: verified
description: "Name matrix legs deterministically and gate branch protection on one aggregate job (needs all legs, if always, fails on any failure/cancel) instead of listing every leg as a required check."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idname", "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/using-a-matrix-for-your-jobs", "https://github.com/re-actors/alls-green"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matrix job names and required checks

**Goal:** add a Python version to the matrix without touching branch protection, and make
"all legs must pass" a single required check.

## 1. How matrix legs are named
Each leg's check name is derived from the job name and the matrix values unless you set `name:`
(`jobs.<id>.name` accepts `matrix` expressions). Control it:
```yaml
jobs:
  test:
    name: test ${{ matrix.os }} py${{ matrix.python }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ['3.11', '3.12']
        include:
          - os: ubuntu-latest
            python: '3.13'
            experimental: true
```
Quote numeric versions: YAML reads an unquoted `3.10` as the number `3.1` (PyYAML: `[3.1, 3.12, '3.10']`).
A matrix key that is missing from a leg (an `include`-only key) evaluates to an empty string in `name:`.

## 2. Why not require each leg
Required checks are listed by name, so adding or removing a leg means editing the ruleset. A job skipped by
a conditional reports Success, but a whole workflow skipped by path/branch filtering or a commit message
leaves its checks "Pending" and blocks the PR (GitHub docs, troubleshooting required status checks).
Require one aggregate instead.

## 3. The aggregate job
```yaml
  ci-ok:
    name: ci-ok
    if: always()                      # run even when legs fail or are skipped
    needs: [test, lint]
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo '${{ toJSON(needs) }}'
          test "${{ contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled') }}" = "false"
```
`needs.*.result` is `success|failure|cancelled|skipped` per upstream job. Decide whether
`skipped` legs count as pass (usually yes for path-filtered jobs). `re-actors/alls-green`
does the same with `allowed-skips` and `allowed-failures` inputs. Require only `ci-ok` in
the ruleset.

Without `if: always()`, `ci-ok` is itself skipped when a leg fails, and GitHub's docs say a job that
depends on a failed job is skipped and "may not block merging", so the aggregate would not catch the
failure. GitHub recommends `always()` with `needs` for required checks.

## 4. Experimental legs
```yaml
    continue-on-error: ${{ matrix.experimental == true }}
```
GitHub docs: this stops a failing leg from failing the workflow run, and the other legs keep running.
Surface the truth by uploading results or using `steps.<id>.outcome` inside the leg.

## 5. Gotchas
- Renaming the job key (`test:` → `unit:`) changes every check name; update rulesets in the
  same PR or merges block.
- `fail-fast: true` (the default) cancels all in-progress and queued legs when one fails → `cancelled`
  results; treat `cancelled` as failure in the aggregate.

## Verify
- [ ] Ruleset lists exactly one required check for the matrix (`ci-ok`).
- [ ] Forcing one leg to fail turns `ci-ok` red; skipping a leg keeps it green.
- [ ] `gh pr checks` shows every leg plus `ci-ok` with stable names.
