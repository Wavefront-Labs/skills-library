---
id: computing-software.networking-hardware-and-wireless.unbound.logging-options
name: logging-options
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, logfile, use-syslog, log-queries, log-replies, verbosity, log-servfail]
level: practitioner
status: docs-checked
description: "Configure Unbound logging: destination, verbosity levels, query and reply logging, SERVFAIL reasons, local-action logging and log rotation."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging options
- `verbosity` (default 1): 0 errors only up to 5, which logs client identification for cache misses. Change at runtime with `unbound-control verbosity N`.
- `logfile` (default empty, stderr): reopened on SIGHUP; setting it turns off `use-syslog` (default yes).
- `log-time-ascii` (no) UTC ASCII timestamps, no effect with syslog; `log-time-iso` (no) ISO8601 when log-time-ascii is also set.
- `log-queries` (no): one line per query; slows the server noticeably.
- `log-replies` (no): one line per reply with resolve time and cache source; `log-destaddr` adds destination address, port and transport; `log-tag-queryreply` adds the words query and reply for easier filtering.
- `log-local-actions` (no): logs local-zone actions.
- `log-servfail` (no): logs why SERVFAIL was returned, at error level.
- `log-thread-id` (no): Linux only.
- `val-log-level` logs validation failures.

Rotation: `unbound-control log_reopen` closes and reopens the log file for logrotate (with syslog it may fail when chrooted).

Foreground debugging: `unbound -d` stays attached to the console; given twice, logging never switches to the log file or syslog and everything goes to stderr.

## Checked

2026-11-08. Read the logging entries of unbound.conf (verbosity through pidfile; not the whole page), the unbound-control manual in full and the unbound -d description. Defaults match; clarified timestamp and double -d behaviour.

Method: documentation only; no commands were run.
