---
id: computing-software.networking-hardware-and-wireless.powerdns.bind-backend-settings
name: bind-backend-settings
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, bind-backend, named-conf, bind-config, bind-check-interval, bind-dnssec-db, native-zones]
level: practitioner
status: docs-checked
description: "Serve BIND-format zones from PowerDNS: bind-config, bind-check-interval, bind-dnssec-db and journal mode, ignore-broken-records, native zones and performance notes."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/bind.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND backend settings

- `bind-config`: the `named.conf` to parse. Only `options` and `zone` blocks and their known directives are used; unknown directives are ignored.
- `bind-check-interval` (default 0, disabled): seconds between zone file change checks. At 0 nothing is rechecked until `pdns_control reload`.
- `bind-dnssec-db`: filename of the DNSSEC metadata database; create it with `pdnsutil create-bind-db`. Secondaries serving presigned zones need it: if empty, the presigned zone is served without DNSSEC and looks bogus.
- `bind-dnssec-db-journal-mode` (default `WAL`): SQLite journal mode; empty leaves it unchanged.
- `bind-hybrid`: keep DNSSEC keys and metadata in another backend (hybrid mode).
- `bind-ignore-broken-records`: `yes` ignores out-of-zone records when loading zone files.

Behaviour:
- Zones with `type native;` (or no type) get no notifies and no AXFR; replicate them out of band, for example with rsync. Supported since 4.1.0.
- A zone is unavailable while it loads. Reloads occur on query or transfer, after the check interval.
- Secondary zones are written to a temporary file, atomically renamed, and parsed only after a successful transfer; the directory must be writable.
- The API is read-only for BIND-hosted zones.
- The packet cache brings no benefit; `distributor-threads=1` can speed things up noticeably.
- In hidden-primary setups, lower `xfr-cycle-interval` so secondaries learn of changes sooner.
- Startup causes no notify storm, but changes found on reload do notify.

## Checked

2026-11-04. Read backends/bind.rst in full and confirmed bind-config directives, bind-check-interval default 0, bind-dnssec-db and its presigned warning, journal mode default WAL, bind-hybrid, bind-ignore-broken-records, native zones since 4.1.0, performance and notify notes. Nothing removed.

Method: documentation only; no commands were run.
