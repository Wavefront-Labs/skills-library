---
id: computing-software.networking-hardware-and-wireless.powerdns.alias-records-expansion
name: alias-records-expansion
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, alias, expand-alias, resolver, outgoing-axfr-expand-alias, apex-cname]
level: practitioner
status: docs-checked
description: "Serve ALIAS records in PowerDNS: resolver and expand-alias settings, apex syntax, SERVFAIL behaviour, outgoing-axfr-expand-alias modes and DNSSEC on AXFR."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/alias.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALIAS records

Needs 4.1.0 or later. Configure:
```
resolver=[::1]:5300
expand-alias=yes
```
Without `resolver`, expansion is disabled. Never point `resolver` at PowerDNS itself (loops). `expand-alias` does not exist in 4.0.x, which always expands direct A/AAAA queries.

Record at the apex: `@ IN ALIAS mywebapp.paas-provider.net.`

- A query for the apex A returns the target's A records. If the target gives SERVFAIL or NXDOMAIN, the answer is SERVFAIL.
- Use one ALIAS per RRset. If several share a name only one is used for resolver queries: the first since 5.1.0, the last before; order depends on the backend.

AXFR, `outgoing-axfr-expand-alias`:
- `no` (default): ALIAS sent as is (type 65401).
- `yes`: A and AAAA of the target are looked up and sent. An unresolvable target fails the AXFR.
- `ignore-errors`: unresolvable targets are omitted, so the transfer completes with an incomplete zone and no standard re-transfer follows; monitor it.
- The serial does not change when the target's addresses change, so secondaries that cannot synthesise ALIAS need periodic re-transfers.

DNSSEC: since 4.0.0 ALIAS is signed on AXFR only, not live-signed. Set `outgoing-axfr-expand-alias=yes` and enable DNSSEC on the primary.

## Checked

2026-11-04. Read the whole ALIAS guide (guides/alias.rst) and confirmed the 4.1.0 requirement, resolver and expand-alias settings, SERVFAIL behaviour, first-versus-last ALIAS before 5.1.0, outgoing-axfr-expand-alias modes, type 65401, and the AXFR-only DNSSEC signing since 4.0.0. Nothing removed.

Method: documentation only; no commands were run.
