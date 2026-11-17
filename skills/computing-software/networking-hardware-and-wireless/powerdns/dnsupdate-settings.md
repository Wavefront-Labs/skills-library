---
id: computing-software.networking-hardware-and-wireless.powerdns.dnsupdate-settings
name: dnsupdate-settings
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnsupdate, rfc2136, allow-dnsupdate-from, tsig-allow-dnsupdate, soa-edit-dnsupdate]
level: practitioner
status: docs-checked
description: "Enable RFC 2136 dynamic updates in PowerDNS: dnsupdate, allow-dnsupdate-from, dnsupdate-require-tsig, forward-dnsupdate, per-zone metadata and SOA-EDIT-DNSUPDATE modes."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnsupdate.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS UPDATE settings

Global (`pdns.conf`):
- `dnsupdate` (default `no`): when off, updates are dropped with no log line.
- `allow-dnsupdate-from` (default `127.0.0.0/8`): space-separated ranges; empty means rely on per-zone metadata. A match in either place grants access.
- `dnsupdate-require-tsig` (5.0.0+, default `no`): reject unsigned updates.
- `forward-dnsupdate` (default `yes`): secondaries forward updates to the domain's masters, trying each until one succeeds.
- `lua-dnsupdate-policy-script`: Lua file defining `updatepolicy`; overrides every other authorization check.

Per-zone metadata (`pdnsutil metadata set <zone> KIND value`; `set-meta` before 5.0):
- `ALLOW-DNSUPDATE-FROM`: permitted source ranges.
- `TSIG-ALLOW-DNSUPDATE`: key names, one `metadata add` each; any listed key satisfies it. If `ALLOW-DNSUPDATE-FROM` is also set, both must pass.
- `FORWARD-DNSUPDATE`: presence enables forwarding for the zone.
- `NOTIFY-DNSUPDATE`: `1` notifies secondaries after each update.
- `SOA-EDIT-DNSUPDATE` (default `DEFAULT`): `DEFAULT` gives YYYYMMDD01 or current+1; `INCREASE` current+1; `EPOCH` Unix time; `SOA-EDIT` uses the zone's SOA-EDIT; `SOA-EDIT-INCREASE` uses that or current+1 if lower.

Supported backends: gmysql, gpgsql, gsqlite3, godbc, and lmdb (5.0.0+).

Caveats: without TSIG enforcement, unsigned updates from allowed addresses are accepted; by default an update can alter any record in the zone, so use the Lua policy for finer control.

## Checked

2026-11-04. Read dnsupdate.rst in full and confirmed the settings and defaults, 5.0.0 gate on dnsupdate-require-tsig, supported backends with lmdb from 5.0.0, per-zone metadata semantics, SOA-EDIT-DNSUPDATE modes and caveats. Nothing removed.

Method: documentation only; no commands were run.
