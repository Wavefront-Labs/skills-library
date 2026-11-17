---
id: computing-software.rpa-and-low-code.n8n.task-runners-setup
name: task-runners-setup
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, task-runners, external-mode, code-node, n8nio-runners, allowlist]
level: advanced
status: docs-checked
description: "Set up n8n task runners in external mode with the n8nio/runners sidecar, broker variables, launcher config and allowlisting extra Code node packages."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/set-up-task-runners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: isolate Code node JavaScript and Python. Task runners are the only isolation between user code and n8n: without them, or in internal mode, anyone who can edit a workflow could read the database, encryption key, credentials and environment variables. Use external mode in production. Internal mode (child process, same uid/gid) is deprecated from n8n 3.0 and logs a startup warning, including when `N8N_RUNNERS_MODE` is unset.

Architecture: runners connect over websocket to a task broker (the n8n main or worker instance); the Code node is the requester. In queue mode every worker needs its own runners sidecar; the main needs one too if `OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=false`.

## Compose reference
n8n container: `N8N_RUNNERS_MODE=external`, `N8N_RUNNERS_BROKER_LISTEN_ADDRESS=0.0.0.0` (default is localhost only), `N8N_RUNNERS_AUTH_TOKEN=<shared secret>`, `N8N_NATIVE_PYTHON_RUNNER=true`. Runners container (`n8nio/runners`, same version as `n8nio/n8n`, n8n 1.111.0 or later): `N8N_RUNNERS_TASK_BROKER_URI=http://n8n-main:5679`, the same `N8N_RUNNERS_AUTH_TOKEN`, and `N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT=15` (seconds idle; 0 disables). `N8N_RUNNERS_ENABLED` is deprecated from 2.0 but required (true) on 1.x; leaving runners off on 1.x runs code in the main process.

## Extra packages
Needs `n8nio/runners:1.121.0` or later. Extend the image:
```dockerfile
FROM n8nio/runners:1.121.0
USER root
RUN cd /opt/runners/task-runner-javascript && pnpm add moment uuid
RUN cd /opt/runners/task-runner-python && uv pip install numpy pandas
COPY n8n-task-runners.json /etc/n8n-task-runners.json
USER runner
```
Then allowlist in the launcher config under `env-overrides`: `NODE_FUNCTION_ALLOW_BUILTIN`, `NODE_FUNCTION_ALLOW_EXTERNAL` (JS runner), `N8N_RUNNERS_STDLIB_ALLOW`, `N8N_RUNNERS_EXTERNAL_ALLOW` and `PYTHONPATH` (Python runner). The default launcher file at `/etc/task-runners.json` is locked down; mount your own over the config path. Debug a custom image with `-e N8N_RUNNERS_LAUNCHER_LOG_LEVEL=debug`.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Set up task runners" page (docs.n8n.io, Markdown version, read in full).
Nothing removed; modes, compose variables, the Dockerfile and the allowlist variables match the page.
