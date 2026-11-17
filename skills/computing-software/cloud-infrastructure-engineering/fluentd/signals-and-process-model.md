---
id: computing-software.cloud-infrastructure-engineering.fluentd.signals-and-process-model
name: signals-and-process-model
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, signals, sighup, sigusr1, sigusr2, supervisor, graceful-reload]
level: practitioner
status: docs-checked
description: "What each Unix signal does to Fluentd (SIGINT/SIGTERM, SIGHUP, SIGUSR1, SIGUSR2, SIGCONT, SIGWINCH) and why signals go to the supervisor."
sources:
  - https://docs.fluentd.org/deployment/signals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd signals
Fluentd runs a supervisor and a worker. Send signals to the supervisor only.

- `SIGINT` / `SIGTERM`: graceful stop. Tries to flush the memory buffer once, no retry on failure. File buffers are not flushed, they persist on disk.
- `SIGUSR1`: flush buffered messages (memory and file) immediately, keep flushing at `flush_interval`, and reopen the log file.
- `SIGHUP`: reload config by gracefully restarting the worker. No socket downtime when sockets come from the `server` helper shared socket, because the supervisor keeps them. Lighter than a full restart when the supervisor need not restart.
- `SIGUSR2`: from v1.18.0 on non-Windows the supervisor does a zero-downtime restart (see `zero-downtime-restart`). Graceful reload (v1.9 and later) is on the worker; the supervisor forwarded it to workers in v1.9 to v1.17 and still does on Windows. Graceful reload ignores `<system>` changes and needs plugins without class variables. The page advises zero-downtime restart or SIGHUP unless there is a special reason.
- `SIGCONT`: dump Fluentd internal status (see `troubleshooting-and-debug-dumps`).
- `SIGWINCH`: cancel Source Only Mode.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/signals and confirmed: signal behaviours, SIGUSR2 version table, SIGHUP socket note. Removed or reworded: the Windows sentence about RPC (not on the page).

Method: documentation only; no commands were run.
