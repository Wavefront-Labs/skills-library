---
id: computing-software.devops-ci-cd.gitlab-runner.runner-security-executors
name: runner-security-executors
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [security, executors, shell-executor, privileged, docker-security]
level: advanced
status: docs-checked
description: "Security risks per executor and what the docs recommend."
sources: ["https://docs.gitlab.com/runner/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security by executor

Any user with the Developer role can compromise the runner environment, intentionally or not. Non-ephemeral runners shared across projects are riskier: one repository can affect others and steal secret variables, including `CI_JOB_TOKEN`.

- Shell: high risk; jobs run with the runner user's permissions. Trusted builds only.
- Docker: considered safe in non-privileged mode. Run jobs as non-root with sudo disabled or SETUID and SETGID dropped, and use `cap_add` and `cap_drop` for finer control.
- SSH: susceptible to MITM because `StrictHostKeyChecking` is missing.
- Parallels: safest, using full virtualization in isolated mode.
- Docker Machine: use `MaxBuilds = 1` with privileged mode.

Cloning a runner shares its token, so the clone can pick up the original's jobs.

## Checked

2026-11-03. Confirmed against per-executor risks, MaxBuilds, cloned-runner warning on Security for self-managed runners.

Method: documentation only; no commands were run.
