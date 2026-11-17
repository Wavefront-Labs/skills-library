---
id: computing-software.devops-ci-cd.semaphore-ui.runners-setup
name: runners-setup
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [runners, remote-runner, registration-token, distributed, semaphore-ui]
level: practitioner
status: docs-checked
description: "Run tasks on separate machines with Semaphore runners: server flags, runner setup, Docker image and tags."
sources:
  - https://semaphoreui.com/docs/admin-guide/runners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Set up Semaphore runners

Goal: execute tasks on a different server than the Semaphore UI.

A runner connects to the server, signals readiness, receives task data, clones the repository, runs Ansible, Terraform, PowerShell and so on, and reports results back. With no runners defined, the server itself runs tasks. With several runners, tasks are distributed randomly among them.

Server configuration:

```json
{
  "use_remote_runner": true,
  "runner_registration_token": "long string of random characters"
}
```

Variables: `SEMAPHORE_USE_REMOTE_RUNNER=True` and `SEMAPHORE_RUNNER_REGISTRATION_TOKEN=...`.

Runner configuration and start:

```bash
semaphore runner setup --config /path/to/config.json
semaphore runner start --config /path/to/config.json
```

Docker runner:

```bash
docker run -d \
  -e SEMAPHORE_WEB_ROOT=https://semaphore.example.com \
  -e SEMAPHORE_RUNNER_REGISTRATION_TOKEN=<token> \
  semaphoreui/runner:latest
```

Mount `/etc/semaphore/requirements.txt` into the runner container for extra Python packages (installed on every start).

Registration can also be done in the web UI or API. In Pro, runners get tags and a template can require a tag so tasks run only on matching runners.

Gotcha: set `runner_registration_token` to a sufficiently complex arbitrary string; the page warns that a weak one is a security risk.

## Checked

2026-11-07. Read in full: the Runners page, from its markdown source in the semaphore-docs repository (admin-guide/runners.md; no snippet files included). Confirmed: how runners work, the no-runner fallback, random distribution, the server options and variables, runner setup and start commands, the Docker run example and requirements.txt mount, the UI/API/CLI registration routes, and Pro runner tags. Removed: the claim that ansible, terraform and git must exist on the runner, the secret-token gotcha wording, and the online-in-Runners-page Verify step, none of which the page states.
Method: documentation only; no commands were run.
