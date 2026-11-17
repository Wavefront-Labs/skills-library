---
id: computing-software.qa-testing-engineering.cypress.cloud-parallelization-and-load-balancing
name: cloud-parallelization-and-load-balancing
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-parallelization, cypress-cloud, load-balancing, ci-build-id, auto-cancellation]
level: practitioner
status: docs-checked
description: "Parallelize Cypress specs across CI machines with Cypress Cloud: --record --parallel, ci-build-id, groups, duration-based load balancing, auto-cancellation."
sources:
  - https://docs.cypress.io/cloud/features/smart-orchestration/parallelization
  - https://docs.cypress.io/cloud/features/smart-orchestration/load-balancing
  - https://docs.cypress.io/cloud/features/smart-orchestration/run-cancellation
  - https://docs.cypress.io/cloud/features/smart-orchestration/spec-prioritization
  - https://github.com/cypress-io/github-action
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cypress Cloud parallelization and load balancing

## How it works
Each CI machine runs `cypress run --record --parallel` with the same **ci-build-id**. Each machine sends its list of spec files to Cypress Cloud, which hands out specs as machines become free, using estimated spec durations from run history so that machines finish together; the run order of specs is not guaranteed. Specs, not tests, are the unit of parallelism, and specs of similar duration parallelize best.

## GitHub Actions
```yaml
jobs:
  e2e:
    runs-on: ubuntu-26.04
    strategy:
      fail-fast: false
      matrix: { containers: [1, 2, 3, 4] }
    steps:
      - uses: actions/checkout@v7
      - uses: cypress-io/github-action@v7
        with:
          record: true
          parallel: true
          group: e2e-chrome
          browser: chrome
          start: npm start
          wait-on: http://localhost:3000
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Cypress derives the CI build ID from provider-specific environment variables (the guide lists them per provider; GitHub Actions is not in that table), and can be overridden with `--ci-build-id`. The action README's parallel example sets only `record`, `parallel` and `group` on the matrix jobs. The action README recommends a Docker image for parallel jobs on GitHub-hosted Ubuntu runners, because a staged runner-image rollout can mix browser major versions and cause Cloud errors; avoid parallel jobs on GitHub-hosted macOS and Windows runners.

## Features
- **Groups**: `--group <name>` separates browsers or configs in one run; the group name must be unique within the run.
- **Spec prioritization** (Business or Enterprise plan): previously failed specs run first.
- **Auto cancellation** (Business or Enterprise plan): cancels the run after a number of failed tests; it can be disabled per run with `--auto-cancel-after-failures false`.
- Flaky-test analytics and Branch Review come with the recorded data.

## Sizing
Optimal machines ≈ total spec duration / target wall time, capped by the longest single spec. Split giant specs; one 8-minute spec sets the floor.

## Gotchas
- The GitHub Actions "Re-run failed jobs" facility is not suited to parallel recording (see the action README); re-run the whole workflow.
- Parallelization needs recording (`--record`) and a Cypress Cloud account.
- The GitHub action only links matrix jobs into one Cloud run; Cloud does the splitting.

## Verify
Cloud run shows balanced machine timelines and all specs accounted for.

## Checked
Checked against the Cypress documentation sources (cypress-io/cypress-documentation, docs/, last commit 2026-10-24, which document Cypress 16; latest release v16.2.0) and the Cypress GitHub Action README (cypress-io/github-action, latest release v7.4.7). Confirmed: `--record --parallel`, CI build ID derivation and `--ci-build-id`, spec distribution and duration estimation, unordered run order, groups, spec prioritization and auto-cancellation plan levels and `--auto-cancel-after-failures`, action inputs `record`, `parallel`, `group`, `browser`, `start`, `wait-on`, `CYPRESS_RECORD_KEY` and `GITHUB_TOKEN`, runner-image caveat and re-run limitation. Removed the unconfirmed third-party alternatives and rebuild-id advice.

Method: documentation only; no commands were run.
