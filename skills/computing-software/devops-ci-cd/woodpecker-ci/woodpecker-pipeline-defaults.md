---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-pipeline-defaults
name: woodpecker-pipeline-defaults
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [defaults, timeouts, approval-mode, cancel-previous]
level: advanced
status: docs-checked
description: "Set server-wide Woodpecker defaults for approvals, cancelling, timeouts and pipeline config paths."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker server-wide pipeline defaults

Several repository settings have server defaults.

- `WOODPECKER_DEFAULT_ALLOW_PULL_REQUESTS` (default `true`).
- `WOODPECKER_DEFAULT_APPROVAL_MODE` (default `forks`): `none`, `forks`, `pull_requests` or `all_events`.
- `WOODPECKER_DEFAULT_CANCEL_PREVIOUS_PIPELINE_EVENTS` (default `pull_request, push`): events cancelled when a new pipeline for the same context (tag or branch) is created.
- `WOODPECKER_DEFAULT_PIPELINE_TIMEOUT` (default 60 minutes): time before a pipeline is killed.
- `WOODPECKER_MAX_PIPELINE_TIMEOUT` (default 120 minutes): the most a repository may set.
- `WOODPECKER_DEFAULT_PIPELINE_CONFIGS` (default `.woodpecker/`, `.woodpecker.yaml`, `.woodpecker.yml`) and `WOODPECKER_DEFAULT_PIPELINE_CONFIG_EXTENSIONS` (default `.yaml`, `.yml`).
- `WOODPECKER_DEFAULT_WORKFLOW_LABELS`: label conditions for agent selection on workflows without labels, such as `platform=linux/amd64,backend=docker`.
- `WOODPECKER_DEFAULT_CLONE_PLUGIN` (default `docker.io/woodpeckerci/plugin-git`), also added to the trusted clone list.

Other limits: `WOODPECKER_MAX_PIPELINE_LOG_LINE_COUNT` (5000) caps lines shown per log; `WOODPECKER_SESSION_EXPIRES` (72h) sets session lifetime; `WOODPECKER_WEBHOOK_SYNC_TIMEOUT` (5s) is how long a webhook waits for pipeline creation before the server answers `202 Accepted` and finishes in the background.

Forge fetch behaviour is tuned with `WOODPECKER_FORGE_TIMEOUT` (30s) and `WOODPECKER_FORGE_RETRY` (3).

Repositories can override most of these in their own project settings, within the server maximums. Restart the server after changing environment variables so the new defaults apply to later pipelines.

## Checked

2026-11-03. Read the Woodpecker server configuration page and confirmed the default and maximum pipeline timeout (60 and 120, in minutes), log line cap 5000, session expiry 72h, webhook sync timeout 5s, forge retry 3 and the WOODPECKER_DEFAULT_* variable names. Nothing removed. 

Method: documentation only; no commands were run.
