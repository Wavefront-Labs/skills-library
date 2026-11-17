---
id: computing-software.database-administration.dragonfly.slowlog-tuning
name: slowlog-tuning
category: computing-software
field: database-administration
product: dragonfly
tags: [slowlog, slowlog-log-slower-than, slowlog-max-len, latency, dragonfly]
level: practitioner
status: docs-checked
description: "Find slow Dragonfly commands with SLOWLOG GET and tune slowlog_log_slower_than and slowlog_max_len."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/server-management/slowlog-get.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The slow log records commands that exceeded an execution time threshold. Execution time may include I/O such as sending the reply.

Flags:

| Flag | Meaning | Default |
| --- | --- | --- |
| `slowlog_log_slower_than` | threshold in microseconds; negative disables the slow log | 10000 |
| `slowlog_max_len` | maximum number of entries | 20 |

Read it with `SLOWLOG GET [count]` (`@admin`, `@dangerous`, `@slow`). It returns up to the latest ten entries by default; `count` limits the number, and `-1` returns all.

Each entry has six values:

1. unique progressive ID
2. unix timestamp when processed
3. execution time in microseconds
4. command arguments
5. client IP and port
6. client name set via `CLIENT SETNAME`

The ID is never reset while the server runs (only a restart resets it), so a script can remember the last ID it handled and avoid processing entries twice.

## Checked

2026-11-04. Confirmed against the Dragonfly SLOWLOG GET page and flags page: threshold and max-length flags with defaults 10000 and 20, negative threshold disabling the log, ACL categories, default of ten entries, `count` and `-1`, the six entry values, ID reset only on restart. Removed the CONFIG SET remark and the SLOWLOG LEN, SLOWLOG RESET and `latencystats` pointers, which these pages do not state.

Method: documentation only; no commands were run.
