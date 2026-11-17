---
id: computing-software.devops-ci-cd.gitlab-runner.runner-register-verify-unregister
name: runner-register-verify-unregister
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [commands, verify, unregister, reset-token, lint]
level: intro
status: docs-checked
description: "Housekeeping commands for registered runners."
sources: ["https://docs.gitlab.com/runner/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runner management commands

- `gitlab-runner register`: add a runner (interactive or `--non-interactive`).
- `gitlab-runner verify`: check that registered runners can connect to GitLab (not whether the service uses them); `--delete` removes runners that were removed from GitLab and updates `config.toml`, so back it up first.
- `gitlab-runner unregister`: remove a registered runner.
- `gitlab-runner reset-token`: replace a runner's token.
- `gitlab-runner lint`: validate `config.toml`.
- `gitlab-runner run`: start the process that picks up jobs.
- `gitlab-runner run-single`: run a single build from a single GitLab instance, with options on the command line or from a configuration file (`-c`, `-r`).

## Checked

2026-11-03. Confirmed against register, verify, unregister, reset-token, lint, run and run-single on the Commands page. Removed the unsourced run-single flags and the closing tip.

Method: documentation only; no commands were run.
