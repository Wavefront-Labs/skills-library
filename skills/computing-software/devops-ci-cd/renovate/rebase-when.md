---
id: computing-software.devops-ci-cd.renovate.rebase-when
name: rebase-when
category: computing-software
field: devops-ci-cd
product: renovate
tags: [rebase-when, rebasing, branch-updates, renovate]
level: practitioner
status: docs-checked
description: "Pick a rebaseWhen value that matches your automerge and branch protection settings."
sources:
  - https://docs.renovatebot.com/configuration-options/#rebasewhen
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`rebaseWhen` controls when Renovate rebases an existing branch:

- `auto`: Renovate picks. It uses `behind-base-branch` if automerge is configured or the repository requires PRs to be up to date, otherwise `conflicted`. On GitHub with a merge queue on the base branch, or GitLab with merge trains, it uses `conflicted`. The default is `auto`.
- `automerging`: `behind-base-branch` when automerging, otherwise `never`.
- `never`: never rebase unless asked manually.
- `conflicted`: rebase only if the branch is conflicted.
- `behind-base-branch`: rebase whenever the branch is one or more commits behind.

```json
{
  "rebaseWhen": "behind-base-branch"
}
```

Cautions from the docs:

- `conflicted` is not recommended with automerge. Two updates merged one after another without being tested together can break the base branch, and if the platform requires up-to-date PRs then automerge stops as soon as a PR falls behind without conflict.
- Avoid `never` because it leaves conflicted branches with stale descriptions and status checks.
- Do not combine `never` with `prCreation=not-pending`; PR creation can stall.

The `rebaseLabel` option names a label that requests a rebase from Renovate.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`rebaseWhen` values, default, cautions, `rebaseLabel`). Removed the rebase checkbox claim and the advice on CI runs and concurrency limits.

Method: documentation only; no commands were run.
