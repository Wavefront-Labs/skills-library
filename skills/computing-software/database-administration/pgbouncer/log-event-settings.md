---
id: computing-software.database-administration.pgbouncer.log-event-settings
name: log-event-settings
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, log-connections, log-stats, verbose, stats-period]
level: practitioner
status: docs-checked
description: "log_connections, log_disconnections, log_pooler_errors, log_stats, stats_period and verbose, with defaults."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose which events and statistics PgBouncer logs.

- `log_connections` (default 1): log successful logins.
- `log_disconnections` (default 1): log disconnections with reasons.
- `log_pooler_errors` (default 1): log error messages the pooler sends to clients.
- `log_stats` (default 1): write aggregated statistics into the log every stats_period. Can be disabled if external monitoring tools collect the same data from SHOW commands.
- `stats_period` (default 60 seconds): how often the averages shown in SHOW commands are updated and how often aggregated statistics are written to the log (subject to log_stats).
- `verbose` (default 0): increase verbosity. Mirrors the -v switch, so `-v -v` equals `verbose=2`. 3 is the highest currently supported.

Example for a quiet instance scraped by an external collector:

```
[pgbouncer]
log_connections = 0
log_disconnections = 0
log_stats = 0
verbose = 0
```

These can be changed at runtime from the admin console, for example `SET log_connections = 1;`. SHOW CONFIG lists each variable with a changeable column telling you whether it can be changed while running (yes) or only at boot (no).

Because stats_period governs the averaging window, avg_ columns in SHOW STATS only change once per period.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
