---
id: computing-software.devops-ci-cd.gitlab-runner.runner-systemd-env-vars
name: runner-systemd-env-vars
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [systemd, init, environment-variables, service, upstart]
level: practitioner
status: docs-checked
description: "Set custom environment variables for the runner service itself."
sources: ["https://docs.gitlab.com/runner/configuration/init/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment for the runner service

The runner uses the Go service library, which detects the init system (systemd, Upstart, System V on Linux, launchd on macOS, Windows services). At install the service file is created: `/etc/systemd/system/gitlab-runner.service` or `/etc/init/gitlab-runner`.

This differs from the `environment` setting, which adds variables to every job. To put a variable in the runner process, for example `GOOGLE_APPLICATION_CREDENTIALS`, create `/etc/systemd/system/gitlab-runner.service.d/env.conf`:
```
[Service]
Environment=GOOGLE_APPLICATION_CREDENTIALS=/etc/gitlab-runner/gce-credentials.json
```
Then `systemctl daemon-reload` and `systemctl restart gitlab-runner.service`.

For Upstart, create `/etc/init/gitlab-runner.override`, `export` the variables and restart.

## Checked

2026-11-03. Confirmed against env.conf and Upstart override on the Init page.

Method: documentation only; no commands were run.
