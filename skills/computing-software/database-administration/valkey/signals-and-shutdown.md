---
id: computing-software.database-administration.valkey.signals-and-shutdown
name: signals-and-shutdown
category: computing-software
field: database-administration
product: valkey
tags: [signals, sigterm, sigint, shutdown, shutdown-timeout, sigusr1, crash]
level: advanced
status: docs-checked
description: "How Valkey handles SIGTERM/SIGINT graceful shutdown, shutdown-timeout, crash signals, killed RDB or AOF children, MISCONFIG state and SIGUSR1."
sources:
  - https://valkey.io/topics/signals/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SIGTERM and SIGINT schedule a graceful shutdown like `SHUTDOWN`: it starts once the current command ends (plus at most 0.1 s). If a long Lua script blocks it, run `SCRIPT KILL`. Steps:
- If replicas lag, pause writers with `CLIENT PAUSE ... WRITE` and wait up to `shutdown-timeout` (default 10 s) for replicas to reach the primary offset.
- Kill any RDB or AOF-rewrite child.
- If AOF is on, `fsync` it.
- If RDB persistence is configured, do a synchronous save (needs no extra memory).
- Remove the PID file and Unix socket, exit with code 0.
If the RDB cannot be saved (or the first AOF rewrite after enabling AOF fails), shutdown aborts and the server keeps running; nothing retries until another SIGTERM or `SHUTDOWN`. To reduce loss when a heavily loaded diskless primary stops, run `FAILOVER` or `CLUSTER FAILOVER` first.

Crash signals SIGSEGV, SIGBUS, SIGFPE, SIGILL: Valkey logs a bug report (stack trace, registers, client state), runs a fast memory test, removes the PID file if daemonized, then re-sends the signal so the default action (core dump) happens.

Killed children: a killed AOF rewrite child is treated as an error, its file discarded, and retried later. A killed or failing RDB child is more severe: the server keeps answering reads but replies to writes with `MISCONFIG` until an RDB save succeeds. To kill the RDB child without that state, send `SIGUSR1`; the parent keeps serving writes.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/signals/ (page text read in full): SIGTERM/SIGINT scheduled shutdown with 0.1 s delay, SCRIPT KILL, CLIENT PAUSE WRITE, shutdown-timeout default 10 s, child kill, fsync, synchronous RDB save, PID file and Unix socket removal, exit 0, failed-save abort, FAILOVER advice, crash signals, killed children, MISCONFIG, SIGUSR1.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
