---
id: computing-software.devops-ci-cd.renovate.automerge-type-branch
name: automerge-type-branch
category: computing-software
field: devops-ci-cd
product: renovate
tags: [automerge-type, branch-automerge, silent-updates, renovate]
level: practitioner
status: docs-checked
description: "Use automergeType branch to merge passing updates without PRs, and understand the fallbacks and CI requirements."
sources:
  - https://docs.renovatebot.com/configuration-options/#automergetype
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`automergeType` defaults to `pr`: Renovate opens a branch and PR, then merges the PR on a later run when checks are green. With `automergeType` set to `branch`, Renovate stays quiet:

1. It creates the branch and waits for test results.
2. It rebases the branch whenever it falls behind.
3. It pushes the commit to the base branch when the branch is up to date and passing.
4. It raises a PR only as a fallback, if tests fail or stay pending too long (25 hours by default, from `prNotPendingHours`).

```json
{
  "automerge": true,
  "automergeType": "branch"
}
```

Caveats:

- Add the `renovate/**` branch pattern to your CI workflow triggers, or tests never run on the branches.
- Branch protection that forbids direct pushes breaks it; stay with PR automerge in that case.
- With GitHub merge queues or GitLab merge trains, branch automerge works only if Renovate is on the bypass list; otherwise the push is rejected and a PR is created.
- The third value, `pr-comment`, only comments on the PR so an external merge bot such as bors-ng can merge.

The upside is fewer notifications, because passing updates leave only commits in the base branch history.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`automergeType` values and default, the branch workflow, 25-hour `prNotPendingHours` fallback, merge queue and merge train bypass note, `pr-comment`) and the Automerge key-concepts page (add `renovate/**` to testing workflows, branch protection limits). Nothing removed.

Method: documentation only; no commands were run.
