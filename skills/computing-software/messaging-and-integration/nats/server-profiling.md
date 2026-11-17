---
id: computing-software.messaging-and-integration.nats.server-profiling
name: server-profiling
category: computing-software
field: messaging-and-integration
product: nats
tags: [profiling, pprof, cpu-profile, memory-profile, nats-server-request-profile, profile-port]
level: practitioner
status: docs-checked
description: "Collect CPU and memory profiles from servers via nats server request profile (system account) and the unauthenticated profiling port."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/profiling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: gather pprof data for a CPU or RAM problem, for troubleshooting or to send to maintainers.

Profiling is an advanced, development-oriented operation; for day-to-day statistics use the monitoring port instead.

Via the nats CLI (must be connected as a system account user). Files are written to the current directory by default (or a directory you pass) and can be opened with `go tool pprof`.
- Memory: `nats server request profile allocs` (all servers), `... allocs ./profiles` (write to a directory), `... allocs --name=servername1`, `--tags=aws`, `--cluster=aws-useast2`. Memory profiles return instantly.
- CPU: `nats server request profile cpu`, same selectors, plus `--timeout=10s` to set how long the CPU profile runs.
- The `--name`, `--tags` and `--cluster` selectors can be combined to target particular servers.

Via the profiling port: enabling it exposes an HTTP profiling endpoint on the server. There is no authentication or authorization on it, and by default it binds to every interface (0.0.0.0), so never expose it to the internet; bind it to localhost or firewall it.

Gotchas: profiles from the right server matter (target the busy node with selectors); CPU profiles need a duration long enough to capture the problem; large clusters produce one file per server.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
