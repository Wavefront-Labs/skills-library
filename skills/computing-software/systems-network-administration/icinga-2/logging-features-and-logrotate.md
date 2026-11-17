---
id: computing-software.systems-network-administration.icinga-2.logging-features-and-logrotate
name: logging-features-and-logrotate
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, logging, mainlog, debuglog, syslog, journald, logrotate]
level: intro
status: docs-checked
description: Configure Icinga 2 logging with the mainlog, debuglog, syslog, journald and windowseventlog features, severities, log file paths, and logrotate with the USR1 signal.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/14-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging features and log rotation
Three kinds of logging: file, syslog (Linux/Unix) and console (stdout on a tty, severity `information` or higher). Loggers are features toggled with `icinga2 feature enable|disable`:

| Feature | Target | Severity |
|---|---|---|
| mainlog | `/var/log/icinga2/icinga2.log` | information or higher |
| debuglog | `/var/log/icinga2/debug.log` | debug or higher |
| syslog | syslog | warning or higher |
| journald | systemd journal | warning or higher |
| windowseventlog | Windows Event Log | information or higher |

`mainlog` is enabled by default.

**Rotation:** packages install a logrotate file, typically `/etc/logrotate.d/icinga2` (local changes survive upgrades). Rotation is daily by default. logrotate sends `USR1` (not the `HUP` reload signal) so Icinga reopens `icinga2.log` (needs `mainlog`), `debug.log` (needs `debuglog`) and `error.log`.

## Checked

2026-11-04. Confirmed against the Icinga 2 features chapter: logging features and severities, daily rotation and USR1 signal.

Method: documentation only; no commands were run.
