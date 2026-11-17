---
id: computing-software.devops-ci-cd.gitlab-runner.runner-signals-and-shutdown
name: runner-signals-and-shutdown
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [signals, sigquit, sighup, graceful-shutdown, systemd]
level: practitioner
status: docs-checked
description: "Signals the runner handles and how to stop it without killing jobs."
sources: ["https://docs.gitlab.com/runner/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Signals and graceful shutdown

Process signals:
- `SIGQUIT`: graceful shutdown; stops taking new jobs and waits for running ones.
- `SIGHUP`: reload `config.toml`.
- `SIGINT` and `SIGTERM`: abort running builds and exit as soon as possible; send twice to exit now (forceful shutdown).

To make a systemd service stop gracefully, create `/etc/systemd/system/gitlab-runner.service.d/kill.conf`:
```
[Service]
KillMode=mixed
TimeoutStopSec=7200
KillSignal=SIGQUIT
```
Then run `systemctl daemon-reload`.

With `KillMode=mixed`, child processes of running jobs do not receive the initial graceful shutdown signal; systemd waits up to two hours, then kills what remains with SIGKILL.

## Checked

2026-11-03. Confirmed against signals on the Commands page and the systemd override on the Init page. Corrected the SIGINT/SIGTERM description; removed the unsourced TimeoutStopSec=infinity.

Method: documentation only; no commands were run.
