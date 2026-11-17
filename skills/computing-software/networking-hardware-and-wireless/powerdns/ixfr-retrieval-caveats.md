---
id: computing-software.networking-hardware-and-wireless.powerdns.ixfr-retrieval-caveats
name: ixfr-retrieval-caveats
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, ixfr, axfr, rectify, empty-non-terminals, presigned]
level: practitioner
status: docs-checked
description: "Enable IXFR retrieval on a PowerDNS secondary with the IXFR metadata, and avoid the DNSSEC switch, NSEC3 and empty non-terminal pitfalls."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/modes-of-operation.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IXFR retrieval caveats

PowerDNS can retrieve IXFR but cannot serve it. Turn it on per zone with the metadata `IXFR` set to `1`:
```
pdnsutil metadata set <zone> IXFR 1
```
(`set-meta` before 5.0.)

Caveats:
- If the primary switches the zone from unsigned to DNSSEC, an IXFR does not set PRESIGNED on the secondary, and NSEC3 mode changes are not picked up. Delete the zone's contents to force a full retrieval.
- IXFR does not remove Empty Non-Terminal records. Run `pdnsutil zone rectify <zone>` afterwards (`pdnsutil rectify-zone` before 5.0).

`pdns_control retrieve <zone>` triggers an immediate retrieval of the zone from the configured primary.

## Checked

2026-11-04. Read the IXFR section and secondary section of modes-of-operation.rst and confirmed the IXFR metadata, retrieve-only (no serving), the DNSSEC and NSEC3 switch warning, the empty non-terminal caveat and the pre-5.0 names. Reworded the pdns_control retrieve line to the page's description (immediate retrieval from the primary) instead of calling it a forced fresh transfer.

Method: documentation only; no commands were run.
