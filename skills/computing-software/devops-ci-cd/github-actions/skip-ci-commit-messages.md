---
id: computing-software.devops-ci-cd.github-actions.skip-ci-commit-messages
name: skip-ci-commit-messages
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, skip-ci, ci-skip, skip-actions, no-ci, commit-message-filter, head-commit-message, bot-commit-loop, skip-checks-trailer, required-checks-skipped, release-commit-skip, workflow-triggers]
level: intro
status: verified
description: "Skip workflow runs via [skip ci] and friends on push/pull_request, break bot-commit loops with commit-message if-guards, and handle the required-status-check consequence."
sources: ["https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/skipping-workflow-runs", "https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#push"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skipping runs with commit messages

**Goal:** stop release-bot commits, doc typos and changelog bumps from burning minutes or
re-triggering themselves.

## 1. Built-in skip strings
Put any of these in the commit message of a push, or in the HEAD commit of a pull request:
`[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, `[actions skip]`.
Or add a `skip-checks: true` (or `skip-checks:true`) trailer: it goes at the end of the message, preceded by
two empty lines, and must be the last trailer if there are others.

Skip instructions apply to `push` and `pull_request` events only (a `pull_request_target` workflow still
runs), and only to the workflow runs triggered by the commit that contains them.

## 2. Consequence: required checks never report
A skipped run creates **no check**, so a branch rule requiring "build" blocks the PR with
"Expected — Waiting for status to be reported". Options:
- Don't skip on PRs; skip only the push-to-main run.
- Instead of skipping, let the workflow run and short-circuit the jobs (they then report
  success) — see §3.

## 3. Conditional skip inside the workflow
```yaml
jobs:
  build:
    if: "!contains(github.event.head_commit.message, '[skip build]')"
```
`head_commit` exists for `push`; for `pull_request` use
`github.event.pull_request.title` or fetch the message in a step. This keeps the run (and
its check) but makes it a 2-second no-op, which satisfies required checks.

## 4. Breaking bot loops
Events caused by the repository's `GITHUB_TOKEN` do not create new workflow runs (exceptions:
`workflow_dispatch` and `repository_dispatch`), which prevents recursion. If you commit with a PAT or App
token to make downstream workflows fire, you must guard the loop yourself:
```yaml
    if: github.actor != 'release-bot[bot]'
```
or commit with `[skip ci]` in the message (`git commit -m "chore: release v1.2 [skip ci]"`).

## 5. Gotchas
- `paths-ignore` is usually the better tool for "docs only" skipping — it is explicit in the
  workflow, not dependent on author discipline.

## Verify
- [ ] A push with `[skip ci]` shows no run; a normal push does.
- [ ] Required checks still pass on PRs (no eternal "Expected").
- [ ] Bot commits do not re-trigger the workflow that produced them.
