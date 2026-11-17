---
id: computing-software.systems-network-administration.rclone.rclone-logging-stats-and-exit-codes
name: rclone-logging-stats-and-exit-codes
category: computing-software
field: systems-network-administration
product: rclone
tags: [logging, log-file, log-rotation, stats, exit-codes, metrics]
level: practitioner
status: docs-checked
description: "Control rclone log levels, log files with rotation, stats output, metrics endpoint and interpret exit codes in scripts."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Levels

Rclone has four levels: `ERROR`, `NOTICE`, `INFO`, `DEBUG`. The default shows ERROR and NOTICE on standard error. `-q` shows only ERROR, `-v` adds INFO (per-transfer information and stats every minute) and `-vv` is DEBUG. `--log-level` sets it explicitly. `--syslog` and `--syslog-facility` log to syslog.

## Log file and rotation

`--log-file` appends to a file (it is not active by default). With logrotate use the `copytruncate` option, since rclone has no rotate signal. Built-in rotation needs `--log-file-max-size` (rounded to MiB); the related flags `--log-file-max-backups`, `--log-file-max-age` and `--log-file-compress` (gzip) are ignored without it.

```console
rclone --log-file rclone.log --log-file-max-size 1M --log-file-max-backups 3
```

`--log-format` takes `date`, `time`, `microseconds`, `UTC`, `longfile`, `shortfile`, `pid` (useful with `mount --daemon`), `nolevel` and `json`; the default is `date,time`. `--use-json-log` gives structured logs.

## Stats and metrics

`--stats 1m` sets the interval, `--stats-one-line` condenses it, `--stats-log-level` chooses the level. `--metrics-addr` publishes OpenMetrics/Prometheus metrics, or use `--rc --rc-enable-metrics`, in which case the rc address is used and `--metrics-*` flags are ignored.

## Exit codes

0 success; 1 uncategorised error; 2 syntax or usage; 3 directory not found; 4 file not found; 5 temporary error (retries might fix it); 6 less serious error; 7 fatal; 8 `--max-transfer` reached; 9 success with nothing transferred (needs `--error-on-no-transfer`); 10 `--max-duration` reached. Rclone only exits non-zero if failures remain after retries (`--retries`).

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
