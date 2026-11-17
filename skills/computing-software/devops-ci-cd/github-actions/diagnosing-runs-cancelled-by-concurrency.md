---
id: computing-software.devops-ci-cd.github-actions.diagnosing-runs-cancelled-by-concurrency
name: diagnosing-runs-cancelled-by-concurrency
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, higher-priority-waiting-request, concurrency, cancel-in-progress]
level: practitioner
status: docs-checked
description: "Explain runs or jobs cancelled by a concurrency group: find the colliding key, why pending runs get replaced, and fix over-broad groups."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency", "https://docs.github.com/en/actions/reference/limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing runs cancelled by a concurrency group

A run or job cancelled by concurrency means another run or job entered the same concurrency group and this one
lost. By default a group holds at most one running and one **pending** item; a newer pending item
replaces the older pending one even with `cancel-in-progress: false` (with `queue: max`, up to 100 can wait).

## Triage
1. Evaluate the group expression for the cancelled run (for example by echoing it in a step) to see which key collided.
2. Find who else uses it: search `.github/workflows` for `concurrency` and compare group expressions.
3. Classify:
   | Symptom | Cause | Fix |
   |---|---|---|
   | PR runs cancel each other across PRs | key is a constant, or uses `github.head_ref`, which is only defined on `pull_request` events | `group: ${{ github.workflow }}-${{ github.head_ref || github.run_id }}` |
   | Deploys skipped, only latest goes out | pending replacement is by default | accept, or use `queue: max` (up to 100 pending) or a lock in the deploy |
   | Different workflows cancel each other | both use `${{ github.ref }}` only | prefix with `github.workflow` |
   | Callee cancels caller | reusable workflow shares key | job-level group in callee |
   | Matrix legs cancel each other | job-level group without matrix value | add `${{ matrix.x }}` |
4. Scheduled runs: `GITHUB_REF` is the default branch for `schedule`, so a cron run and a push to main collide when the key is `github.ref`.
   Add `github.event_name` to the key if they must both run.

## Gotchas
- By default (`queue: single`) concurrency is not a FIFO queue: every intermediate pending run except the newest is cancelled. `queue: max` queues up to 100 in first-in-first-out order (not combinable with `cancel-in-progress: true`).

## Verify
- [ ] After fixing, two pushes to different PRs both complete.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- One running plus one pending per group, replacement of the pending item, case-insensitive group names, and FIFO ordering: confirmed in the concurrency reference text (reusable actions-group-concurrency).
- queue single/max with a limit of 100 and the invalid combination with cancel-in-progress true: confirmed in the same text and the limits page (applies to GitHub.com plans).
- github.head_ref only on pull_request, the run_id fallback, and the github.workflow prefix pattern: confirmed in the same text.
- GITHUB_REF is the default branch for schedule: confirmed in the events reference.
- Removed the quoted UI annotation, the gh run list command and the required-check claim, which no fetched page documents.

Method: documentation only; no commands were run.
