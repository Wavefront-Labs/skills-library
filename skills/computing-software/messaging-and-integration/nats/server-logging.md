---
id: computing-software.messaging-and-integration.nats.server-logging
name: server-logging
category: computing-software
field: messaging-and-integration
product: nats
tags: [logging, log-file, logfile-size-limit, syslog, logrotate, sigusr1]
level: practitioner
status: docs-checked
description: "Configure nats-server logs: debug/trace flags, log_file, logfile_size_limit and max_num, syslog targets, logrotate with SIGUSR1."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/logging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get the right log detail to the right place and rotate it safely.

Flags: `-l/--log FILE`, `-T` (timestamps, default true; `-T false` disables), `-s/--syslog`, `-r/--remote_syslog`, `-D/--debug`, `-V/--trace` (raw protocol), `-VV` (also traces the system account), `-DV`, `-DVV`. Examples: `nats-server -DV -m 8222 -l nats.log`; syslog via UDP `nats-server -r udp://localhost:514` or `-r syslog://<hostname>:<port>`.

Config file equivalents:
```
debug: false
trace: true
logtime: false
logfile_size_limit: 1GB
logfile_max_num: 100
log_file: "/tmp/nats-server.log"
```

Rotation: since v2.1.4 the server rotates itself when the file exceeds `logfile_size_limit`; backups carry the original name plus a `.yyyy.mm.dd` style suffix. Alternatively use logrotate with a `postrotate` step `kill -SIGUSR1 $(cat /var/run/nats-server.pid)`. That signal does not kill the server: it makes it reopen its log file after rotation. The pid file location is wherever the server's `-P/--pid` or config wrote it.

Gotcha: `-V` traces the raw protocol, which includes message traffic and so can expose payloads in logs; use debug and trace for diagnosis, not as defaults.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
