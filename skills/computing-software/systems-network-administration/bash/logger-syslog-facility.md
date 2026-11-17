---
id: computing-software.systems-network-administration.bash.logger-syslog-facility
name: logger-syslog-facility
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, logger-syslog-facility, logger-priority, shell-scripting]
level: practitioner
status: docs-checked
description: "Send shell script messages to syslog or journald with logger, setting tag, priority, facility and structured output."
sources:
  - https://man7.org/linux/man-pages/man1/logger.1.html
  - https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logger priorities and facilities
**Goal:** log centrally from scripts.
```bash
logger -t backup -p user.notice "backup started"
logger -t backup -p user.err    "backup failed rc=$rc"
logger --id=$$ -t myjob -- "message with -dashes"       # log PID, protect leading dash
some_cmd 2>&1 | logger -t some_cmd -p daemon.info       # no message argument: stdin is logged
journalctl -t backup --since "1 hour ago"
logger -p local0.info -t app "to a custom facility"
logger -s --no-act -t app "dry run, echoed to stderr only"
```
- `-p` takes a number or a `facility.level` pair; the default is `user.notice`.
- Levels: emerg alert crit err warning notice info debug (panic, error, warn are deprecated synonyms). Facilities include auth, authpriv, cron, daemon, ftp, lpr, mail, news, syslog, user, uucp and local0 to local7; `kern` cannot be generated from userspace and is converted to `user`.
- `-t` marks every line with the tag (default: the login user name). `journalctl -t` filters on that syslog identifier.
- `--id=$$` is recommended by the man page in scripts that send several messages; systemd listening on /dev/log may override the PID from socket credentials unless logger is root and the PID exists.
- `--` ends the argument list so a message can begin with a hyphen. `-s` also writes the message to stderr; `--no-act` skips the actual log write (for testing with `-s`).
- Default maximum message size is 1KiB, changed with `-S/--size`; the size includes the syslog header and the receiver must support larger sizes.
- `--journald` reads journal fields from stdin or a file and ignores options such as priority; put `PRIORITY=` in the input.
- Exit status is 0 on success and non-zero on error; with `--socket-errors=off` lost messages still exit 0.
- Self-check: `journalctl -t backup -n1` shows the line.

## Checked
Checked 2026-11-08 against logger(1) (options, default priority, levels and facilities, --id, --size, --journald, --no-act, exit status) and journalctl (-t, --since). Removed: "about 1-8 KB depending on daemon" (page says 1KiB default), and that logger always writes via /dev/log on systemd hosts.

Method: docs-only read of cited pages, 2026-11-08
