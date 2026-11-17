---
id: computing-software.database-administration.influxdb.configure-influxd-logging
name: configure-influxd-logging
category: computing-software
field: database-administration
product: influxdb
tags: [logs, log-level, flux-log-enabled, logfmt, journalctl, stdout]
level: practitioner
status: docs-checked
description: "Where influxd logs go (stdout, journald, STDOUT in /etc/default/influxdb), the log-level values, and how to turn on the Flux query log."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

InfluxDB writes logs to stdout. Redirect to a file when running manually (file output uses logfmt):

```sh
influxd 1> /path/to/influxdb.log
```

As a service, logs go where the service manager sends them; on most Linux systems:

```sh
sudo journalctl -u influxdb.service
```

When run as a service, stdout is discarded (sent to /dev/null) by default. To write a file, set the `STDOUT` variable in the startup script `/etc/default/influxdb` and restart:

```conf
STDOUT=/var/log/influxdb/influxd.log
```

Log level (`log-level`): `debug` (debug, info, error), `info` (default: info and error), `error` (errors only).

```sh
influxd --log-level=info          # or INFLUXD_LOG_LEVEL=info
```

Enable Flux query logging with `flux-log-enabled` (`--flux-log-enabled` or `INFLUXD_FLUX_LOG_ENABLED=true`). It goes to stdout with other logs. The page suggests logrotate for rotation and hutils or lnav for working with logs.

## Checked

2026-11-08: confirmed against the Markdown source of the cited page in the InfluxData docs repository (read in full): stdout default, file redirect and logfmt, journalctl, the `STDOUT` variable in `/etc/default/influxdb` (the sysvinit case), log-level values and default, `INFLUXD_LOG_LEVEL`, `flux-log-enabled` forms, and the tool suggestions. Removed the claim that Flux logging is off by default, which the page does not state.
Method: documentation only; no commands were run.
