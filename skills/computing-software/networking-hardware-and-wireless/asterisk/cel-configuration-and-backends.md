---
id: computing-software.networking-hardware-and-wireless.asterisk.cel-configuration-and-backends
name: cel-configuration-and-backends
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, cel, channel-event-logging, cel-conf, cel-custom, cel-odbc, celgenuserevent, billing]
level: practitioner
status: docs-checked
description: "Configure Channel Event Logging in cel.conf and choose backends (AMI, RADIUS, cel_custom, ODBC, PGSQL, SQLite3, TDS), and generate USER_DEFINED events with CELGenUserEvent."
sources:
  - https://docs.asterisk.org/Configuration/Reporting/Channel-Event-Logging-CEL/
  - https://docs.asterisk.org/Configuration/Reporting/Channel-Event-Logging-CEL/CEL-Configuration-Files/
  - https://docs.asterisk.org/Configuration/Reporting/Channel-Event-Logging-CEL/CEL-Applications-and-Functions/
  - https://docs.asterisk.org/Configuration/Reporting/Channel-Event-Logging-CEL/CEL-Specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CEL configuration and backends
CEL records granular channel events (designed with billing in mind) and is an alternative to CDRs when you need detailed logs. You can control which applications are tracked and which events are raised, plus a configurable date format. The billing logic is entirely yours.

General settings live in `cel.conf`; CEL publishes records only to backends enabled there.

Backends and files:
- Manager (AMI): `[manager]` in `cel.conf`; record type appears as `EventName`.
- RADIUS: `[radius]` in `cel.conf`.
- Custom CSV: `cel_custom.conf`.
- ODBC: `cel_odbc.conf`.
- PostgreSQL direct: `cel_pgsql.conf`.
- SQLite3: `cel_sqlite3_custom.conf`.
- TDS (Sybase, Microsoft SQL Server): `cel_tds.conf`.

Record groups: stand-alone (channel start/end, answer, hangup, application start/end, user defined, linked ID end), interaction (bridge enter/exit, forward, park start/end, pickup), and meta-records (blind transfer, attended transfer, local channel optimization). The peer field is used only in bridge enter/exit.

`CELGenUserEvent` raises `USER_DEFINED` with `eventtype` and `userdeftype`. The name is unrestricted, so reusing a standard event name will look like that event.

Most CEL fields come from `CHANNEL()`; the old `CEL` function may exist, check `core show function CEL`.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Channel-Event-Logging-CEL, CEL-Configuration-Files, CEL-Applications-and-Functions, CEL-Specification) and confirmed the commands, options, defaults and names stated above. Added CEL-Specification as a source.

Method: documentation only; no commands were run.
