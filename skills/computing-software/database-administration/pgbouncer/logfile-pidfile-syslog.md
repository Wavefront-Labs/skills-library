---
id: computing-software.database-administration.pgbouncer.logfile-pidfile-syslog
name: logfile-pidfile-syslog
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, logging, logfile, pidfile, syslog]
level: intro
status: docs-checked
description: "logfile, pidfile and syslog settings: daemon requirements, log rotation with SIGHUP and the syslog facility options."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure where PgBouncer writes logs and its PID.

- `logfile` (default not set): the log file. For daemonization (-d), either logfile or syslog must be set. The file is kept open, so after rotation run `kill -HUP` or the console command `RELOAD;`. On Windows the service must be stopped and started. Setting logfile does not by itself stop logging to stderr; use -q or -d.
- `pidfile` (default not set): without it, daemonization (-d) is not allowed.
- `syslog` (default 0): toggles syslog. On Windows the event log is used instead.
- `syslog_ident` (default pgbouncer, the program name): name used when sending logs to syslog.
- `syslog_facility` (default daemon): one of auth, authpriv, daemon, user, local0-7.

```
[pgbouncer]
logfile = /path/to/pgbouncer.log
pidfile = /path/to/pgbouncer.pid
syslog = 1
syslog_ident = pgbouncer
syslog_facility = daemon
```

On Windows, to use the event log set `syslog = 1` and first register the event library with `regsvr32 pgbevent.dll` (unregister with `regsvr32 /u pgbevent.dll`).

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a cross-reference line.

Method: documentation only; no commands were run.
