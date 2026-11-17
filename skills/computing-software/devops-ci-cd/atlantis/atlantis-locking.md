---
id: computing-software.devops-ci-cd.atlantis.atlantis-locking
name: atlantis-locking
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [locking, repo-locks, unlock, locks-ui, discard-plan]
level: practitioner
status: docs-checked
description: "Understand Atlantis directory and workspace locks, repo_locks modes and how to release a lock."
sources: ["https://www.runatlantis.io/docs/locking", "https://www.runatlantis.io/docs/repo-level-atlantis-yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis locking

Running `plan` locks that directory and Terraform workspace until the PR is merged or closed or the plan is deleted. Another PR planning the same directory and workspace gets an error linking to the PR holding the lock. Only that directory and workspace are locked, not the repo.

Why: apply runs before merge, so `main` no longer reflects live infrastructure; locking blocks competing changes and lets you re-plan and re-apply on the same branch after a failed apply. Atlantis locks are separate from Terraform state locks, which prevent concurrent applies on one state.

Configure per project with `repo_locks`:

```yaml
repo_locks:
  mode: on_apply
```

Modes: `disabled`, `on_plan` (default), `on_apply`. The older boolean `repo_locking` is deprecated.

View locks in the Locks UI at the Atlantis URL. Unlock by commenting `atlantis unlock` (removes all locks on the PR and discards plans) or via the link at the bottom of a plan comment, then Discard Plan and Unlock for a single plan. After discarding, run `plan` again before `apply`.

Before `apply`, Atlantis checks the global apply lock and fails closed if the lock backend is unreachable. Drift detection or remediation run through the API with `PR: 0` takes and releases working directory locks but creates no PR-level locks, so they do not appear in the UI.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Locking, Repo Level atlantis.yaml (repo_locks). Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
