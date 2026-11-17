---
id: computing-software.devops-ci-cd.gitlab-runner.runner-ssh-executor
name: runner-ssh-executor
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [ssh-executor, remote-host, identity-file, maintenance-mode]
level: intro
status: docs-checked
description: "What the SSH executor does and its limits."
sources: ["https://docs.gitlab.com/runner/executors/ssh/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SSH executor

The SSH executor connects to a remote machine and runs the job script there. Configure `[runners.ssh]` with `user`, `host`, and `password` or `identity_file` (or both).

The runner does not implicitly read `identity_file` from `~/.ssh/id_(rsa|dsa|ecdsa)`; specify it explicitly.

The project source is checked out to `~/builds/<short-token>/<concurrent-id>/<namespace>/<project-name>`.

To upload job artifacts, install `gitlab-runner` on the host you connect to.

The executor is in maintenance mode, and the security guide notes it is susceptible to MITM attacks because of the missing `StrictHostKeyChecking` option.

## Checked

2026-11-03. Confirmed against SSH executor settings, build path and maintenance mode on SSH executor and Executors pages, MITM note on Security.

Method: documentation only; no commands were run.
