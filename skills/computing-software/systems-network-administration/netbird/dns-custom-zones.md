---
id: computing-software.systems-network-administration.netbird.dns-custom-zones
name: dns-custom-zones
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, custom-zones, dns-records, split-horizon, distribution-groups]
level: practitioner
status: docs-checked
description: "Host private DNS records in NetBird Custom Zones: zone settings, A/AAAA/CNAME records, TTL, precedence over nameservers and limitations."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/custom-zones.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Custom Zones hold private records that NetBird distributes to peers and resolves locally; nothing is forwarded externally.

Create: DNS > Zones > Add Zone.
- Domain: an FQDN such as `services.company.internal`; cannot be changed later and cannot conflict with the peer DNS domain.
- Distribution Groups: at least one; only these peers receive the zone, and membership changes update distribution.
- Enable Search Domain: off by default; lets `api` expand to `api.services.company.internal`.
- Enable DNS Zone: on by default; off holds records without distributing (testing).

Records: Hostname, type A, AAAA or CNAME, value, and TTL (default 300 seconds; lower propagates faster but costs more queries).

Edit via the three-dot menu. Deleting a zone deletes all its records.

Precedence: a zone beats a nameserver whose match domain matches; the nameserver is not queried for that domain.

Limitations:
- Domain is immutable (delete and recreate).
- CNAME cannot coexist with A or AAAA for the same hostname.
- Zones with no records are not distributed.
- Peers in unmanaged DNS mode (DNS Settings group or `--disable-dns`) do not resolve zone records.

Uses: internal service discovery, environment isolation, split-horizon DNS.

## Checked

2026-11-04: read the Custom Zones page in full. Confirmed zone settings and defaults, record types, the 300 second TTL default, delete behaviour, precedence over nameservers and all five limitations. Nothing removed.

Method: documentation only; no commands were run.
