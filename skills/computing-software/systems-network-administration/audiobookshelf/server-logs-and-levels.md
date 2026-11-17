---
id: computing-software.systems-network-administration.audiobookshelf.server-logs-and-levels
name: server-logs-and-levels
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [logs, log-level, crash-logs, scan-logs, debugging]
level: practitioner
status: docs-checked
description: "Find and use Audiobookshelf daily, scan and crash logs, and pick the right log level (Warn, Info, Debug)."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/server-logs.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/server-settings.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three log levels exist: `Warn`, `Info`, `Debug`. New installs default to `Info`.

Locations:

- `/metadata/logs/daily` - daily logs as JSON files, viewable in the web client.
- `/metadata/logs/scans` - library scan logs for debugging scanning issues.
- `/metadata/logs/crash_logs.txt` - server crashes, which can hold details that never reach the daily log because the server died.

Logs are stored only for the current level. If the server is set to `Info`, no `Debug` entries exist.

If `crash_logs.txt` is empty, check the logs for however you run the server, for example Docker container logs.

Related: `QUERY_LOGGING` (`log` or `benchmark`) logs SQL queries.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Server Logs page, and Environment Configuration page.

Method: documentation only; no commands were run.
