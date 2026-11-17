---
id: computing-software.database-administration.patroni.patroni-logging-configuration
name: patroni-logging-configuration
category: computing-software
field: database-administration
product: patroni
tags: [patroni, logging, json-logs, log-rotation, configuration]
level: practitioner
status: docs-checked
description: "Configure the Patroni log section: format, JSON logs, rotation, per-module levels and heartbeat deduplication."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control Patroni log output.

```
log:
  type: json
  format:
    - message
    - module
    - asctime: '@timestamp'
    - levelname: level
  static_fields:
    app: patroni
```

Settings and defaults:
- `type`: `plain` (default) or `json` (needs the jsonlogger package).
- `level`: default INFO. `traceback_level`: default ERROR; set DEBUG to see tracebacks only when `log.level=DEBUG`.
- `format`: default `%(asctime)s %(levelname)s: %(message)s`. For JSON it may be a list of LogRecord field names, or a dictionary to rename fields. `dateformat`, `static_fields` (JSON only).
- `max_queue_size`: two-step logging uses an in-memory queue, default 1000 records, enough for about 1h20m.
- `dir`: log directory (must exist and be writable). When set, defaults to retaining 4 files of 25MB; tune with `file_num` and `file_size` (bytes triggering rolling). `mode`: file permissions such as 0644.
- `loggers`: per Python module levels, for example `patroni.postmaster: WARNING`, `urllib3: DEBUG`.
- `deduplicate_heartbeat_logs` (default false): suppress identical successive heartbeat lines such as "Lock owner: ... and no action". Warning: the HA loop execution time is valuable for diagnosing failovers caused by resource exhaustion; no log is produced for it unless the leader changes.

Environment equivalent for deduplication: `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS`.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (log section): type, level, traceback_level, format, dateformat, static_fields, max_queue_size, dir, file_num, file_size, mode, loggers, and the FAQ for `deduplicate_heartbeat_logs` and `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS`. Removed: the generic `PATRONI_LOG_*` and `PATRONI_LOG_LEVEL` names, which the fetched pages do not list.

Method: documentation only; no commands were run.
