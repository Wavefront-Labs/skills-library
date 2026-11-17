---
id: computing-software.devops-ci-cd.semaphore-ui.git-client-and-retries
name: git-client-and-retries
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [git, git-client, git-attempts, go-git, repositories, semaphore-ui]
level: practitioner
status: docs-checked
description: "Choose git_client cmd_git or go_git and tune git_attempts retries with exponential backoff."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git client and retry settings

Goal: control how Semaphore clones and updates repositories before each run.

| Option | Variable | Description |
|---|---|---|
| `git_client` | `SEMAPHORE_GIT_CLIENT` | `cmd_git` (default, system `git` binary) or `go_git` (pure Go client). |
| `git_attempts` | `SEMAPHORE_GIT_ATTEMPTS` | Tries for clone and pull before the task fails. Default 4; 1 means no retry. |

When a clone or pull fails and tries remain, Semaphore waits with exponential backoff starting at 1 second, doubling per attempt, capped at 60 seconds, and logs a line like `Git pull failed (...), retrying in 2s`.

```json
{ "git_client": "cmd_git", "git_attempts": 8 }
```

Guidance:
- Intermittent outages of GitHub, GitLab or self-hosted servers: raise `git_attempts`.
- Immediate persistent failures (wrong credentials, missing repo, bad branch): retries do not help; fix the cause.
- `cmd_git` needs git installed on the server or runner and honors forwarded proxy variables (see the forwarded variables skill).

Verify: a task log shows the retry lines on a flaky connection and the final clone succeeds, or the failure appears after the configured number of attempts.

## Checked

2026-11-04: checked against the configuration reference and host config page. Every claim is stated there.

Method: documentation only; no commands were run.
