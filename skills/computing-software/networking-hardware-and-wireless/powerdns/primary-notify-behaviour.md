---
id: computing-software.networking-hardware-and-wireless.powerdns.primary-notify-behaviour
name: primary-notify-behaviour
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, primary, native, notify, pdns-control, also-notify, modes-of-operation]
level: practitioner
status: docs-checked
description: "Run PowerDNS Authoritative as native or primary: enabling primary, zone types that notify, TSIG on NOTIFY, pdns_control notify."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native and primary operation

Native (the default): PowerDNS neither sends nor reacts to notifications; the backend (for example database replication) moves the data. Database secondaries are normally read-only; PowerDNS only needs write access for zone transfers or when a frontend edits records.

Primary (off by default, enable with `primary` in `pdns.conf`):
- Zones must be of type `PRIMARY` (or `MASTER`). Only those are notified, unless `secondary-do-renotify` is on.
- Since 4.0.0 a NOTIFY carries a TSIG record when the zone uses TSIG and the feature is enabled.
- With DNSSEC zones and non-PowerDNS secondaries, review the `soa-edit` metadata.
- Define NS and A records for every secondary.
- In SQL, set `domains.type` to `MASTER` for primaries.

Overrides:
```
pdns_control notify <domain>
pdns_control notify-host <domain> <ip>
```
`notify` tells all detected secondaries; `notify-host` pings an arbitrary IP, handy together with `also-notify`.

Per RFC 1996 the primary announces a change and the secondary then checks the serial. PowerDNS finds secondary IPs by several methods, so duplicate notifications can happen and are harmless. Backends either detect changes themselves or let operators flag zones as changed.

## Checked

2026-11-08. Read docs/modes-of-operation.rst in full (native, primary, secondary, IXFR, autoprimary and axfrfilter sections). Confirmed native behaviour, primary being off by default, PRIMARY or MASTER zone types and secondary-do-renotify, the 4.0.0 TSIG on NOTIFY, soa-edit advice, NS and A records, and pdns_control notify and notify-host. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
