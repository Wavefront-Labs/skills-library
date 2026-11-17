---
id: computing-software.cloud-infrastructure-engineering.fluentd.http-rpc-endpoints
name: http-rpc-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, rpc, rpc-endpoint, flush-buffers, config-reload, windows]
level: practitioner
status: docs-checked
description: "Manage Fluentd over HTTP RPC with rpc_endpoint instead of signals: flushBuffers, config.reload, zeroDowntimeRestart and stop endpoints."
sources:
  - https://docs.fluentd.org/deployment/rpc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd HTTP RPC
Disabled by default. Enable in `<system>` (cannot be used with `--no-supervisor`); useful where signals are poorly supported, such as Windows:
```
<system>
  rpc_endpoint 127.0.0.1:24444
</system>
```
```
curl http://127.0.0.1:24444/api/plugins.flushBuffers
{"ok":true}
```
Each endpoint returns JSON. Equivalents:
- `/api/processes.interruptWorkers` (SIGINT, v1.0) and `/api/processes.killWorkers` (SIGTERM, v1.0): stop the daemon.
- `/api/processes.zeroDowntimeRestart` (SIGUSR2, v1.18; not on Windows).
- `/api/processes.flushBuffersAndKillWorkers` (SIGUSR1 then SIGTERM, v1.0).
- `/api/plugins.flushBuffers` (SIGUSR1, v1.0).
- `/api/config.reload` (SIGHUP, v1.0).
- `/api/config.gracefulReload` (v1.9): the pre-v1.18 SIGUSR2 replacement; prefer zeroDowntimeRestart or config.reload unless you have a special reason.

## Checked

2026-11-04. Confirmed against the Fluentd RPC page (docs.fluentd.org/deployment/rpc): rpc_endpoint config, default off, --no-supervisor note, endpoint table with signals and versions. Nothing removed.

Method: documentation only; no commands were run.
