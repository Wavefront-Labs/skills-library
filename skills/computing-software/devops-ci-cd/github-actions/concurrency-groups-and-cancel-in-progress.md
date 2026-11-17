---
id: computing-software.devops-ci-cd.github-actions.concurrency-groups-and-cancel-in-progress
name: concurrency-groups-and-cancel-in-progress
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, concurrency, concurrency-group, cancel-in-progress, concurrency-expression, concurrency-group-key, conditional-cancel-in-progress, pending-job-cancelled, concurrency-queue, workflow-level-concurrency, pr-concurrency, cancel-superseded, github-workflow-ref, head-ref-fallback, cost-control]
level: practitioner
status: verified
description: "Build concurrency group keys from workflow, ref and PR so superseded CI runs cancel, main never cancels, and you understand the one-pending-run queue behaviour."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#concurrency"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrency groups and cancel-in-progress

**Goal:** every new push to a PR cancels the now-pointless previous run, while pushes to
`main` and releases queue instead of cancelling.

## 1. The standard key
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```
- `github.workflow` scopes per workflow (its `name:` or file path) so CI and Deploy do not
  cancel each other.
- `pull_request.number || github.ref` gives one group per PR, and per branch/tag otherwise.
- The boolean expression makes cancellation conditional: PRs cancel, `main` queues.
Allowed contexts in workflow-level `concurrency`: `github`, `inputs`, `vars`; job-level adds `needs`,
`strategy`, `matrix`. Not `env` or `secrets`. Group names are case-insensitive (`prod` and `Prod` are one
group) and group names are scoped to the repository.

## 2. Queue semantics
A group holds **at most one running and one pending** run/job. A newly queued run replaces any existing
`pending` one (the running one is untouched) when `cancel-in-progress` is false; `cancel-in-progress: true`
also cancels the running one. So on a hot branch you never get a backlog — only the newest waits.
The current docs also describe a `queue: max` option (up to 100 pending runs, not combinable with
`cancel-in-progress: true`); actionlint 1.7.12 does not know the key yet.

## 3. Job-level groups
```yaml
jobs:
  deploy:
    concurrency:
      group: deploy-${{ inputs.environment }}
      cancel-in-progress: false
```
Workflow-level and job-level groups are independent; a job can serialise across *different*
workflows by sharing a group string (e.g. `terraform-prod`). Group names are per repository.

## 4. Variations
- Cancel only on non-default branches: `cancel-in-progress: ${{ github.ref != format('refs/heads/{0}', github.event.repository.default_branch) }}`.
- Merge queue: group on `github.event.merge_group.head_ref` (a field of the `merge_group` payload) so each
  queue entry is separate.
- Matrix legs: `group: test-${{ matrix.os }}-${{ github.ref }}` (job-level) if legs must not
  overlap across runs.
- Dispatch runs that must never be cancelled: omit `cancel-in-progress` and use a unique
  group including `github.run_id`.

## 5. Gotchas
- `cancel-in-progress: true` on `main` can cancel a deploy mid-flight — never enable it
  unconditionally on a workflow that deploys.

## Verify
- [ ] Two rapid pushes to a PR: first run cancelled, second completes.
- [ ] Two rapid pushes to `main`: both complete, second waited.
- [ ] Deploy workflow never shows a cancelled run caused by concurrency.
