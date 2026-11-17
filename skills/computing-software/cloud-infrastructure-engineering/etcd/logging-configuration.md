---
id: computing-software.cloud-infrastructure-engineering.etcd.logging-configuration
name: logging-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [logging, logger, zap, log-level, log-outputs, structured-logs, debug, capnslog]
level: intro
status: docs-checked
description: "Configure etcd logging: --logger zap, --log-level, --log-outputs destinations and rotation."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Logging flags (v3.5 Configuration options page):

- `--logger`: default `zap`; currently the only supported value, for structured logging.
- `--log-level`: default `info`; supports `debug`, `info`, `warn`, `error`, `panic` or `fatal`.
- `--log-outputs`: default `default`. Specify `stdout` or `stderr` to skip journald logging even when running under systemd, or a comma-separated list of output targets.
- `--enable-log-rotation` (default `false`): enable log rotation of a single `--log-outputs` file target.
- `--log-rotation-config-json`: configures rotation when enabled. Default `{"maxsize": 100, "maxage": 0, "maxbackups": 0, "localtime": false, "compress": false}`: MaxSize in MB, MaxAge in days (0 is no limit), MaxBackups (0 is no limit), LocalTime (use the computer's local time) and Compress (gzip).

Every flag has an environment variable with the `ETCD_` prefix in upper snake case (for example `ETCD_LOG_LEVEL`). Command-line flags take precedence over environment variables, and if a configuration file is given all flags and environment variables are ignored.

## Checked

2026-11-08. Read in full: etcd v3.5 Configuration options page. Confirmed every flag, default and value list above. Removed: the 3.4 --log-output rename, the log message catalogue (apply request took too long, slow fdatasync, lost leader and others), the restart-to-change-verbosity advice and the debug-volume remark (not on the page).
Method: documentation only; no commands were run.
