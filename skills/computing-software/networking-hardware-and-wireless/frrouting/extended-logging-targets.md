---
id: computing-software.networking-hardware-and-wireless.frrouting.extended-logging-targets
name: extended-logging-targets
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, log-extended, rfc5424, journald, syslog, structured-data]
level: advanced
status: docs-checked
description: "Create FRR extended logging targets with formats, destinations (syslog, journald, file, unix, fd), priority, facility, timestamp and structured-data options."
sources:
  - https://docs.frrouting.org/en/latest/extlog.html
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended logging targets
`log extended EXTLOGNAME` creates a target; it then needs a destination. Multiple targets can exist; remove with `no`.

Formats (`format FORMAT`): `rfc5424` (ISO 8601 timestamps, time zone, structured data), `rfc3164` (legacy BSD, 1-second granularity), `local-syslog` (rfc3164 without hostname), `journald` (native, structured).

Destinations:
- `destination none` disables the target, keeping its configuration.
- `destination syslog [supports-rfc5424]` writes to `/dev/log`; on Linux `supports-rfc5424` must be set manually.
- `destination journald`
- `destination <stdout|stderr|fd <0-63>|envvar WORD> [format FORMAT]` uses a descriptor open at daemon start.
- `destination file PATH [create [{user WORD|group WORD|mode PERMS}]|no-create] [format FORMAT]`; ownership and mode apply only when FRR creates the file.
- `destination unix PATH [format FORMAT]` for a UNIX socket (stream, seqpacket or dgram auto-detected).

Format defaults to RFC5424 for stdout, stderr, fd, envvar and file.

Options: `priority PRIORITY` (default debugging); `facility FACILITY` (default daemon; the global `log facility` does not affect extended targets); `timestamp precision (0-9)` (rfc5424 and journald only); `timestamp local-time` (default UTC); `structured-data <code-location|version|unique-id|error-category|format-args>` (`unique-id` and `error-category` on by default).

Messages logged while a unix, syslog or journald receiver is down are lost unless socket activation keeps the socket open.

## Checked

2026-11-04. Confirmed against the FRR Extended Logging Target page and Basic Commands page: formats, destinations, format defaults, priority, facility, timestamp and structured-data options and defaults, receiver-down caveat. Removed the unsupported 'one per target' wording.
Method: documentation only; no commands were run.
