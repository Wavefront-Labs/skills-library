---
id: computing-software.systems-network-administration.nagios-core.logging-and-debug
name: logging-and-debug
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, logging, log-file, log-rotation-method, log-archive-path, use-syslog, debug-level, debug-verbosity, debug-file, troubleshooting]
level: practitioner
status: docs-checked
description: "Nagios Core main-config logging: log_file, rotation and archive path, what to log, and debug_level bitmask categories with debug_verbosity and debug_file."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configmain.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging and debugging

## Log
- `log_file`: main log. `log_rotation_method` `n/h/d/w/m` (default n none); `log_archive_path` is the directory for rotated files.
- `use_syslog` 0/1.
- What to log: `log_notifications`, `log_service_retries`, `log_host_retries`, `log_event_handlers`, `log_external_commands` (default 1), `log_passive_checks` (default 1).

## Debug
- `debug_level`: bitwise OR of categories; default 0 (nothing); `-1` logs everything. Documented bits: config 2, host/service checks 16, notifications 32, external commands 128, macros 2048.
- `debug_verbosity`: 0 basic, 1 more (default), 2 highly detailed.
- `debug_file`: output file. `max_debug_file_size` in bytes; when exceeded the file is renamed with `.old`, replacing any previous `.old`.

## Practice
Enable one category, reproduce, read `debug_file`, then reset to 0, since debug files grow quickly. Use `macros` (2048) to see expanded command lines, `notifications` (32) to see why a notice was filtered.

Related: `computing-software.systems-network-administration.nagios-core.notification-filters`.

## Checked

2026-11-04. Confirmed against the main configuration page: log_rotation_method n/h/d/w/m (default n), log_archive_path, use_syslog, log_external_commands and log_passive_checks default 1, debug_level bit values (2, 16, 32, 128, 2048, -1, default 0), debug_verbosity 0/1/2 (default 1), max_debug_file_size in bytes with .old rename. Removed the claim that history/trends/avail CGIs need the archive path (not on the page).

Method: documentation only; no commands were run.
