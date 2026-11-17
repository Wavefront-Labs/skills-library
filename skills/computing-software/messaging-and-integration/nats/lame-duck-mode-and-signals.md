---
id: computing-software.messaging-and-integration.nats.lame-duck-mode-and-signals
name: lame-duck-mode-and-signals
category: computing-software
field: messaging-and-integration
product: nats
tags: [lame-duck, signals, reload, sigusr2, graceful-shutdown, nats-server-signal]
level: practitioner
status: docs-checked
description: "Gracefully drain a server with nats-server --signal ldm and use signal commands for reload, reopen, quit, stop."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/signals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shut down or reconfigure a running server cleanly.

Lame duck mode is the production-recommended shutdown: `nats-server --signal ldm` (SIGUSR2). The server stops accepting new connections, waits a 10 second grace period, then evicts clients gradually over the period set by the `lame_duck_duration` option. This avoids a thundering herd of TLS reconnects hitting the other servers. The server sends clients a message; some maintainer-supported clients expose a callback so apps can prepare for the short outage.

Signal table (`nats-server --signal <cmd>` on Unix):
- `ldm` = SIGUSR2, lame duck;
- `quit` = SIGINT and `term` = SIGTERM, graceful stop;
- `stop` = SIGKILL, immediate;
- `reload` = SIGHUP, reload config;
- `reopen` = SIGUSR1, reopen log file (for rotation);
- plain `kill -SIGQUIT` kills with a stack dump.

Multiple processes: give a PID or pid file, `nats-server --signal stop=<pid>` or `stop=/path/to/pidfile`; from 2.10.0 a glob such as `ldm=12*` matches several PIDs. Windows uses the Windows service control instead.

Gotchas: without a PID the command needs `pgrep` to find the single process; `stop` gives no graceful close.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
