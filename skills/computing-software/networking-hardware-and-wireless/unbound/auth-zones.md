---
id: computing-software.networking-hardware-and-wireless.unbound.auth-zones
name: auth-zones
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, auth-zone, zone-transfer, zonefile, zonemd, root-zone-copy]
level: advanced
status: docs-checked
description: "Hold a local copy of a zone in Unbound with auth-zone: primaries, URLs, notify, upstream and downstream use, fallback and ZONEMD checks."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# auth zones
An `auth-zone:` clause (repeatable) gives Unbound zone data to answer from. The closest matching name wins.

- `name:` zone name.
- `primary:` (alias `master`) IP or hostname, repeatable; accepts `@port` and `#auth-name` for AXFR over TLS.
- `url:` HTTP/HTTPS zonefile URL, repeatable, tried in order.
- `allow-notify:` extra NOTIFY sources; primaries and URLs are allowed by default.
- `zonefile:` file name; none if unset.
- `fallback-enabled` (default no) falls back to normal resolution when lookups fail (for example DNSSEC validation failure) or the zone has expired.
- `for-downstream` (default yes) answers clients authoritatively; `for-upstream` (default yes) serves recursion from the local data.
- `zonemd-check` (default no) verifies ZONEMD; `zonemd-reject-absence` (default no) makes a missing ZONEMD a failure.

unbound-control: `auth_zone_reload zone` re-reads the zone file (cached validated entries stay; use `flush_zone`), `auth_zone_transfer zone` probes primaries by SOA serial, and `list_auth_zones` shows expiry and serial. Counters `num.query.authzone.up` and `.down` track use.

## Checked

2026-11-08. Read the auth-zone section of the unbound.conf manual in full (rst source) and the unbound-control commands list_auth_zones, auth_zone_reload, auth_zone_transfer and the authzone counters. Defaults confirmed. Reworded fallback-enabled to match the manual (applies when lookups fail or the zone expires).

Method: documentation only; no commands were run.
