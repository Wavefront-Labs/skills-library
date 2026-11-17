---
id: computing-software.database-administration.pgbackrest.logging-options
name: logging-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, logging, log-level-console, log-level-file, log-path]
level: practitioner
status: docs-checked
description: "Console, file and stderr log levels, the log path, and which log files async archiving writes."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get useful logs without noise.

Levels, lowest to most verbose: `off`, `error`, `warn`, `info`, `detail`, `debug`, `trace`. Three outputs:

- `log-level-console` (default `warn`).
- `log-level-file` (default `info`).
- `log-level-stderr` (default `off`): levels that go to stderr instead of stdout; timestamp and process are omitted there.

`log-path` defaults to /var/log/pgbackrest. If `log-level-file=off` no log path is needed. `log-timestamp` (default y) controls timestamps.

```
pgbackrest --stanza=demo --log-level-console=detail restore
```

Examples in the user guide use `detail` to show per-file actions such as `backup file ...`.

Log file names are per stanza and command, for example `demo-archive-push-async.log` and `demo-archive-get-async.log` for async archiving.

Packaged logrotate configuration may rotate as a specific user via `su`; if pgBackRest runs as a different user, update it or logrotate fails with a permission error.

Use `--log-level-console=info` to see begin and end lines that echo the options in force, which is the quickest way to confirm which configuration values a command used.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (logrotate, async log names). Removed: the 'restore file ... exists and matches backup' example. 

Method: documentation only; no commands were run.
