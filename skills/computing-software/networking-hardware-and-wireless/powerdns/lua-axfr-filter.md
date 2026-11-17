---
id: computing-software.networking-hardware-and-wireless.powerdns.lua-axfr-filter
name: lua-axfr-filter
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua, axfr, axfrfilter, lua-axfr-script, secondary]
level: advanced
status: docs-checked
description: "Filter records on incoming AXFR in PowerDNS with LUA-AXFR-SCRIPT: pdnsutil metadata, axfrfilter(remoteip, zone, record), return codes."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lua AXFR filter

Enable on the secondary zone:
```
pdnsutil metadata set <zone> LUA-AXFR-SCRIPT /path/to/script.lua
```
(`set-meta` before 5.0.) The script must exist and be syntactically valid, otherwise the transfer is aborted.

Define `axfrfilter(remoteip, zone, record)`; it runs once for each incoming record. Record type constants live in the `pdns` table, for example `pdns.TXT`.

Return values:
- `0` plus a table: replace the record with the table's records (an empty table drops it).
- `1` plus a table: keep the record and append the table's records.
- `-1` plus an empty table: handle the record normally.

Typical uses named by the docs: normalise SOA values, rewrite the serial to YYYYMMDDnn, enforce a consistent NS RRset, add a timestamp TXT record.

## Checked

2026-11-08. Read the 'Modifying a secondary zone using a script' section of docs/modes-of-operation.rst plus the rest of that file. Confirmed the metadata command and its pre-5.0 set-meta form, the missing or invalid script aborting the transfer, the pdns table, return codes 0, 1 and -1 and the listed uses. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
