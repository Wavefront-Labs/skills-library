---
id: computing-software.networking-hardware-and-wireless.frrouting.logging-destinations
name: logging-destinations
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, logging, log-file, syslog, log-stdout, log-level, timestamp]
level: practitioner
status: docs-checked
description: "Configure FRR logging to file, stdout and syslog, set severity levels, facility, timestamps and priority display, and view logging state."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging destinations
Levels: emergencies, alerts, critical, errors, warnings, notifications, informational, debugging (the default is typically debugging).

- `log file [FILENAME [LEVEL]]` logs to a file, e.g. `log file /var/log/frr/bgpd.log informational`. `no` disables it.
- `log daemon DAEMON file [FILENAME [LEVEL]]` does file logging for one daemon.
- `log stdout [LEVEL]`; if systemd is connected to stdout, FRR switches to journald extended logging.
- `log syslog [LEVEL]` uses the system `syslog()` API. The page recommends `log extended` with `destination syslog [supports-rfc5424]` where possible.
- `log facility [FACILITY]` sets the syslog facility (default `daemon`).
- `log record-priority` adds severity to messages sent to file, stdout or terminal monitor (not syslog). Default off.
- `log timestamp precision [(0-6)]` sets fractional-second digits; default is 1-second accuracy.
- `log immediate-mode` gives unbuffered log and debug output.
- `log commands` logs every typed command, including passwords on the command line.
- `log trap LEVEL` is deprecated; `log monitor` is deprecated and does nothing.
- `send log [level LEVEL] MESSAGE` and `logmsg LEVEL MESSAGE` inject messages.
- `show logging` shows configuration and destination status.

Startup equivalents: `--log <stdout|syslog|file:/path>` and `--log-level <level>`. `--command-log-always` always logs commands and disallows `no log commands`.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page: log levels, file, daemon, stdout, syslog, facility, record-priority, timestamp precision, immediate-mode, commands, deprecated trap and monitor, send log, logmsg, show logging, --log and --log-level, --command-log-always. Nothing changed.
Method: documentation only; no commands were run.
