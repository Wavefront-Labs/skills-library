---
id: computing-software.collaboration-platform-administration.vikunja.config-logging
name: config-logging
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, log-section, log-level, structured-json-logs, log-database-queries]
level: practitioner
status: docs-checked
description: "Tune Vikunja logging: destinations, levels, text or structured JSON, and the separate database, HTTP, event and mail log channels for debugging."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core options:
- `log.enabled` (default true), `log.path` (default the `logs` folder in the rootpath): a folder where all the logfiles should go.
- `log.standard` default `stdout`; values `stdout`, `stderr`, `file`, `off`.
- `log.level` default `INFO`; `ERROR`, `WARNING`, `INFO`, `DEBUG` (case-insensitive; `CRITICAL` = ERROR, `NOTICE` = INFO).
- `log.format`: `text` (default) or `structured` to output JSON.

Channels, each with a destination (`stdout`, `stderr`, `file` or `off`) and a `...level` option that defaults to `log.level`:
- `log.database` (default off) and `log.databaselevel`: database queries, useful for debugging.
- `log.http` (default `stdout`) and `log.httplevel`: requests are logged at INFO, requests failing with 4xx at WARNING, 5xx at ERROR.
- `log.events` (default off) and `log.eventslevel` (ERROR, INFO, DEBUG).
- `log.mail` (default off) and `log.maillevel`: does not log mail contents.

## Checked

2026-11-04: every option, default and value list checked against config-raw.json (log section). Removed the "debug recipe" and Docker `docker logs` advice, which the source does not state.

Method: documentation only; no commands were run.
