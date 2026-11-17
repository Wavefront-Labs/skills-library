---
id: computing-software.devops-ci-cd.github-actions.merge-queue-workflows-with-merge-group
name: merge-queue-workflows-with-merge-group
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, merge-group-event, merge-group-concurrency, merge-queue, merge-queue-workflow, checks-requested, merge-group-head-ref, merge-group-base-sha, queue-batching, required-checks-merge-queue, gh-readonly-queue, merge-queue-skipped-checks, rulesets, branch-protection]
level: practitioner
status: verified
description: "Make CI run on merge-queue groups: add the merge_group trigger, scope concurrency per queue entry, keep check names stable so required checks resolve, and avoid the paths-filter skip trap."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#merge_group", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merge-queue workflows with merge_group

**Goal:** the queue builds each candidate merge against the *real* future `main`, your
required checks pass on that build, and PRs merge without a human re-running anything.

## 1. Trigger
```yaml
on:
  pull_request:
  merge_group:
    types: [checks_requested]     # the only type
```
Without `merge_group` your required checks are not triggered when a PR enters the queue, so the merge
fails because the required status check is never reported (GitHub docs). The queue builds temporary
branches whose names begin with `gh-readonly-queue/<base_branch>`; for the event, `github.ref` is the ref
of the merge group and `github.sha` is the SHA of the merge group. The webhook payload's `merge_group`
object has `head_sha`, `head_ref`, `base_ref`, `base_sha` and `head_commit`.

## 2. Concurrency per entry
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.merge_group.head_ref || github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name != 'merge_group' }}
```
Never cancel queue runs: the queue may hold several batched entries at once and each needs
its own result.

## 3. Required checks must have the same name
The ruleset requires a check by **name** (job `name:` or key). The job must exist and
report on `merge_group` events. Two traps:
- A workflow skipped by path filtering leaves its checks "Pending", which blocks a PR that requires
  them (GitHub docs). `paths` filters exist only for `push` and `pull_request`, so keep `merge_group:`
  free of them, and for docs-only PRs gate inside an always-running job (for example with
  `dorny/paths-filter`) so the required job still reports.
- Matrix jobs: require the aggregate job (`ci-ok`) that `needs:` all legs, not the legs.

## 4. Skip work not needed in the queue
```yaml
jobs:
  lint:
    if: github.event_name != 'merge_group'    # already validated on the PR
  e2e:
    if: github.event_name == 'merge_group'    # expensive; run only on the final merge candidate
```
The queue is the right place for slow full-suite tests; PRs can run the fast subset.

## 5. Gotchas
- Queue settings live under the "Require merge queue" branch protection setting (or the ruleset rule):
  merge method, build concurrency (1-100), only merge non-failing pull requests, status check timeout,
  and min/max merge limits (1-100).
- A merge queue cannot be enabled with branch protection patterns containing a wildcard (`*`).
- For third-party CI, trigger on pushes to branches with the `gh-readonly-queue/<base_branch>` prefix.

## Verify
- [ ] A PR added to the queue gets a run with `event: merge_group` and all required checks.
- [ ] Docs-only PRs still merge from the queue (no eternal "Expected").
- [ ] `gh run list --event merge_group` shows no cancelled runs.
