---
id: computing-software.qa-testing-engineering.test-automation.staged-pipeline-and-fail-fast-ordering
name: staged-pipeline-and-fail-fast-ordering
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [staged-pipeline, fail-fast, ci-pipeline, test-impact-analysis, deployment-pipeline]
level: practitioner
status: docs-checked
description: "Order CI test stages for fast feedback: cheap checks first, fail-fast rules, parallel stages, test impact selection on PRs and full suites on main or nightly."
sources:
  - https://playwright.dev/docs/test-cli
  - https://docs.pytest.org/en/stable/how-to/failures.html
  - https://martinfowler.com/articles/continuousIntegration.html
  - https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fail-fast ordering and staged test pipelines

**Goal:** developers get the most likely failure signal in minutes, and expensive suites run only when cheaper ones pass.

## Stage order (typical)
1. **Static:** lint, format, type check, secret scan.
2. **Unit and component:** parallelised.
3. **Build artefact once** (image/package) and reuse it in later stages.
4. **Integration and contract:** containers, Pact verification.
5. **E2E smoke on a deployed preview.**
6. **Full regression, performance, security scans:** on merge to main, nightly, or before release.

## Fail-fast mechanics
- Stage dependencies: GitHub `needs:`; later jobs skip if earlier ones fail.
- Within a stage, run jobs in parallel; let them finish (matrix `fail-fast: false`) when you want the full picture, cancel (`fail-fast: true`) when cost matters.
- Inside a runner: `pytest -x` / `--maxfail=5`, Playwright `--max-failures=10` stop early when something is fundamentally broken.
- Cancel superseded runs on new pushes (GitHub `concurrency: { group: ${{ github.ref }}, cancel-in-progress: true }`).

## Selecting tests on PRs
- Path filters (`on.pull_request.paths`) to skip unaffected suites.
- Test impact analysis: run tests affected by changed files (`jest --changedSince=origin/main`, Playwright `--only-changed`), with a full run on main to catch misses.

## Measure
Track median PR pipeline time and time to first failure; set a target for time to first meaningful signal.

## Verify
A lint error fails the pipeline early without running E2E, PR pipelines meet the time target, and full suites still run on main or nightly.

## Checked
2026-10-28. Confirmed: matrix `fail-fast`, `concurrency` with `cancel-in-progress`, `on.pull_request.paths` (GitHub workflow syntax page); `pytest -x` and `--maxfail` (pytest failures page); Playwright `--max-failures` and `--only-changed` (test CLI and CI pages); `jest --changedSince` (Jest CLI page). Removed: stage durations and the 10 and 2 minute targets, GitLab, Jenkins, pytest-testmon, Nx and Bazel claims (not in fetched pages), and the blocked ISTQB source.
Method: documentation only; no commands were run.
