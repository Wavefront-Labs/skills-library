---
id: computing-software.devops-ci-cd.github-actions.events-triggers-and-filters
name: events-triggers-and-filters
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, workflow-triggers, on-events, workflow-dispatch, repository-dispatch, schedule-cron, event-filters, path-filters, branch-filters, tag-filters, paths-ignore, activity-types, pull-request, pull-request-target, push, release-event, workflow-run, issue-comment, github-event, event-payload, manual-trigger, dispatch-inputs, default-branch-only]
level: practitioner
status: verified
description: "Choose and filter GitHub Actions triggers: activity types, branch/path/tag filters, workflow_dispatch inputs, repository_dispatch, schedule quirks, workflow_run chaining and the default-branch rules."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows", "https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#on", "https://docs.github.com/en/webhooks/webhook-events-and-payloads"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Events, triggers and filters

**Goal:** the workflow runs exactly when it should, on the ref it should, and not on the
dozens of pushes/PR edits that waste minutes.

## 1. Activity types — the default is not "all"
Most events default to a subset. `pull_request` defaults to `opened, synchronize, reopened`;
you must add `ready_for_review`, `labeled`, `closed` explicitly:
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  release:
    types: [published]
  issue_comment:
    types: [created]
```
For release pipelines GitHub's docs recommend `published`: `created`, `edited` and `deleted` do not trigger
workflows for draft releases, and `prereleased` does not fire for pre-releases published from drafts
(`published` does).

## 2. Branch, tag and path filters
```yaml
on:
  push:
    branches: [main, 'release/**']
    tags: ['v*.*.*']
    paths: ['src/**', 'package.json', '!**/*.md']
  pull_request:
    branches: [main]            # TARGET branch for PRs, not the head branch
    paths-ignore: ['docs/**']
```
Rules that bite:
- If you define only `branches` (or only `tags`) on `push`, the workflow does not run for events affecting
  the other kind of ref; define neither and both trigger. With both `branches` and `paths` the workflow
  runs only when both filters match. Path filters are not evaluated for tag pushes.
- `paths` and `paths-ignore` cannot be combined for the same event; use `!` negation inside `paths`.
- The changed-file list uses two-dot diffs for pushes and three-dot diffs for pull requests. Limits (GitHub.com
  docs): a push of more than 1,000 commits always runs the workflow, so does a diff that times out, and if
  the diff has more than 3,000 files and the matching files are not among the first 3,000 the workflow
  does **not** run.
- A workflow skipped by path filtering, branch filtering or a commit message leaves its checks "Pending",
  which blocks a PR that requires them. Use `dorny/paths-filter` inside an always-running job, or make the
  job itself conditional and still succeed, instead of filtering at the `on:` level.

## 3. Events that only fire from the default branch
`schedule`, `workflow_dispatch` (the UI shows the "Run workflow" button only if the file is on the default
branch), `repository_dispatch`, `issue_comment`, `issues` and `workflow_run` are documented as only triggering
a run if the workflow file exists on the default branch (and `GITHUB_REF` is the default branch for most of
them). Testing a schedule change on a feature branch does nothing until merged.

## 4. workflow_dispatch and repository_dispatch
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]
        required: true
      dry_run:
        type: boolean
        default: true
```
Use as `${{ inputs.environment }}` (or `github.event.inputs.*`, where booleans become strings). On GitHub.com
the maximum is 25 top-level inputs (10 on GHES) and 65,535 characters in total.
Trigger: `gh workflow run deploy.yml -f environment=staging --ref main`.

`repository_dispatch` is the cross-repo/webhook hook — POST `/repos/{o}/{r}/dispatches` with
`{"event_type":"deploy","client_payload":{...}}` using a token that can write to that repository (the
workflow's own `GITHUB_TOKEN` is limited to its repository, but dispatch events it creates do start runs).
Filter with `on: repository_dispatch: types: [deploy]`; payload at `github.event.client_payload`.

## 5. schedule
```yaml
on:
  schedule:
    - cron: '17 3 * * 1-5'   # UTC only
```
- Not guaranteed on time: delays are likely at the start of every hour and queued runs can be dropped
  under load. Pick an odd minute (`17`, not `0`).
- Disabled automatically after 60 days without repository activity in public repos.
- Runs on the latest commit of the default branch; `github.ref` is that branch.

## 6. workflow_run — chaining and the "secrets on forks" trick
```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
jobs:
  report:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
```
The workflow started by `workflow_run` can access secrets and write tokens even if the triggering workflow
could not (GitHub docs), and `GITHUB_REF` is the default branch. Treat any artifact downloaded from the
triggering run as **untrusted input** (fork code produced it). `github.event.workflow_run.head_sha` and
`head_branch` identify the original commit. `workflow_run` cannot chain more than three levels of
workflows.

## 7. pull_request vs pull_request_target
`pull_request` from a fork: no secrets except `GITHUB_TOKEN`, whose write permissions are reduced to
read by default. `pull_request_target` runs in the context of the default branch of the base repository
with a read/write token, which keeps unsafe PR code out of the workflow definition; never check out and
execute PR head code in it (`ref: ${{ github.event.pull_request.head.sha }}` plus a build step hands
your secrets to the PR author). Use it only for labelling/commenting on PR metadata.

## 8. Preventing loops and noise
- Events caused by `GITHUB_TOKEN` (for example a push) do **not** create new workflow runs, except
  `workflow_dispatch` and `repository_dispatch`. If you need a follow-on run after a bot commit, push with
  an App token or PAT — and then guard against infinite loops with `if: github.actor != 'my-bot[bot]'`.
- `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]`, `[actions skip]` in the commit message (the HEAD
  commit for a PR) skip `push`/`pull_request` workflows.
- Add `concurrency` to cancel superseded PR runs (see the concurrency skill).

## 9. Inspecting what fired
`${{ github.event_name }}`, `${{ github.ref }}`, `${{ github.ref_type }}`, `${{ github.head_ref }}`
(PRs only), `${{ github.base_ref }}`. Dump everything once: `run: echo '${{ toJSON(github.event) }}'`
(fine for public data, never with secrets in the payload).

## Verify
- [ ] A doc-only commit does not start the build workflow, yet required checks still pass.
- [ ] A tag push `v1.2.3` triggers the release workflow and a branch push does not.
- [ ] `gh workflow run` with inputs appears in the run's `inputs` context.
- [ ] No workflow uses `pull_request_target` with a checkout of the PR head.
