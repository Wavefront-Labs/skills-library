---
id: computing-software.cloud-infrastructure-engineering.fluentd.logging-output-and-rotation
name: logging-output-and-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, logging, log-file, rotate-age, rotate-size, json-log, ignore-same-log-interval]
level: practitioner
status: docs-checked
description: "Send Fluentd logs to a file, rotate them, switch to JSON format, and suppress repeated log messages with ignore_repeated_log_interval and ignore_same_log_interval."
sources:
  - https://docs.fluentd.org/deployment/logging
  - https://docs.fluentd.org/deployment/system-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd log output, format and rotation
Default output is stdout. File: `fluentd -o /path/to/log_file`, or since v1.18.0 `<system><log> path /path/to/log_file </log></system>`.

Format via `<log>` in `<system>`: `format` is `text` (default) or `json`; `time_format` default `%Y-%m-%d %H:%M:%S %z`.
```
<system>
  <log>
    format json
    time_format %Y-%m-%d
  </log>
</system>
```
Rotation is off by default. Set `rotate_age` (integer generations, or `daily`, `weekly`, `monthly`; default 7) and/or `rotate_size` (bytes, default 1048576) in `<log>` (from v1.13.0). Omit both and rotation stays disabled; omitting one uses its default. CLI equivalents: `--log-rotate-age`, `--log-rotate-size` (size applies when age is an integer). On Windows rotated files are named `log-supervisor-0.log`, `log-0.log` ... `log-N.log`.

`forced_stacktrace_level` (1.19.0, default `none`): forces stacktrace lines to a given level, e.g. to keep stacktraces out of alerting on the log file.

Suppress noise from an unstable destination:
```
<system>
  ignore_repeated_log_interval 60s
  ignore_same_log_interval 60s
</system>
```
`ignore_repeated_log_interval` (since v1.10.2) suppresses repeated messages; `ignore_same_log_interval` (since v1.11.3) also covers actions that emit several different messages per retry.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/logging, https://docs.fluentd.org/deployment/system-config and confirmed: log file path, format, rotation defaults and Windows file names, forced_stacktrace_level, ignore_*_log_interval. Removed or reworded: nothing.

Method: documentation only; no commands were run.
