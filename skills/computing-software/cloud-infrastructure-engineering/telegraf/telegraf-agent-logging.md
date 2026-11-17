---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-agent-logging
name: telegraf-agent-logging
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [logging, logfile, log-rotation, debug, logformat]
level: practitioner
status: docs-checked
description: "Covers Telegraf agent logging settings: debug, quiet, logformat, logfile and rotation, time zone and the Windows eventlog format."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/agent/", "https://docs.influxdata.com/telegraf/v1/administer/monitor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Agent logging

By default Telegraf logs to stderr, or to the journal under systemd. Change this in `[agent]`.

## Settings

- `debug` (false): debug-level logging.
- `quiet` (false): only error-level messages.
- `logformat` (`"text"`): `text`, `structured`, or on Windows `eventlog`.
- `structured_log_message_key` (`"msg"`): message key for structured logs.
- `logfile`: file to log to; unset means stderr. Ignored for `eventlog`.
- `logfile_rotation_interval` (`"0h"`): time-based rotation, disabled by default.
- `logfile_rotation_max_size` (`"0MB"`): size-based rotation, disabled by default.
- `logfile_rotation_max_archives` (5): archives to keep; `-1` keeps all.
- `log_with_timezone`: such as `America/Chicago`, or `local`.

```toml
[agent]
  logfile = "/var/log/telegraf/telegraf.log"
  logfile_rotation_max_size = "10MB"
  logfile_rotation_max_archives = 5
```

Per-plugin overrides use the plugin `log_level` option. The global flags `--debug` and `--quiet` also exist.

Under systemd read logs with `journalctl --unit telegraf`. On Windows, service startup messages go to the Windows event log (Event Viewer, Windows Logs, Application); runtime messages go to the configured log target.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Agent logging settings and defaults (agent reference), journalctl and Windows event log notes (run-as-service). Removed: nothing.

Method: documentation only; no commands were run.
