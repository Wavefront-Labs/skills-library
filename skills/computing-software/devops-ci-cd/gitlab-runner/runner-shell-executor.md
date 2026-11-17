---
id: computing-software.devops-ci-cd.gitlab-runner.runner-shell-executor
name: runner-shell-executor
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [shell-executor, trusted-builds, host-permissions]
level: intro
status: docs-checked
description: "What the shell executor does and why it suits only trusted builds."
sources: ["https://docs.gitlab.com/runner/executors/shell/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shell executor

The shell executor runs jobs directly on the machine where the runner is installed, as if you typed the commands in a terminal. With `concurrent = 1` and one `[[runners]]` section it is the simplest possible setup.

Jobs run with the permissions of the GitLab Runner user. The security guide states that high-security risks exist to the runner host and network, and that builds can steal code from other projects run on the same server, so use it only for running trusted builds.

Dependencies must be installed on the host yourself.

The executor is in maintenance mode; the Docker, Kubernetes, Docker Autoscaler and Instance executors are the active ones.

## Checked

2026-11-03. Confirmed against shell executor behaviour on Fleet scaling and Security, and maintenance mode on Executors.

Method: documentation only; no commands were run.
