---
id: computing-software.networking-hardware-and-wireless.powerdns.tinydns-backend
name: tinydns-backend
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, tinydns, cdb, tinydns-dbfile, locations, tai-adjust]
level: practitioner
status: docs-checked
description: "Serve a tinydns CDB file from PowerDNS: dbfile, tai-adjust, notify-on-startup, ignore-bogus-records, locations, cache-ttl."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/tinydns.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tinydns backend

Settings (defaults in brackets):
- `tinydns-dbfile` (`data.cdb`): the data file; the page recommends setting it.
- `tinydns-tai-adjust` (11): seconds added to the TAI base to account for leap seconds; the default was last updated on 1 January 2017.
- `tinydns-notify-on-startup` (no): notify at startup (the page says all the primary nameservers); this might cause broadcast storms.
- `tinydns-ignore-bogus-records` (no): keep running when the CDB holds corrupt RDATA. Those records are not served (tinydns would still send them). Mainly useful in primary mode.
- `tinydns-locations` (yes): with no, locations are ignored and everything, including AXFR, returns all records. With yes, AXFR returns only records without a location.

Caveats:
- Location restrictions on name-server (dot-prefixed) lines are treated differently from tinydns: PowerDNS ignores those lines and the SOA, so it takes no authority over that zone. Restrict other data, or disable locations.
- Timestamps and locations work properly only with `cache-ttl` and `query-cache-ttl` set to 0. Timestamps tolerate `cache-ttl` but the returned TTL is not exact.
- Locations exist for IPv4 only.
- In primary mode the whole CDB is scanned every `xfr-cycle-interval`; raise it for large files.

## Checked

2026-11-08. Read in full: PowerDNS docs backends/tinydns.rst. Confirmed all five settings with their defaults, the tai-adjust note, the locations and AXFR behaviour, the dot-line location caveat, the cache-ttl and query-cache-ttl interaction, IPv4-only locations and the CDB scan interval. Reworded the startup-notify and tai-adjust lines to match the page.

Method: documentation only; no commands were run.
