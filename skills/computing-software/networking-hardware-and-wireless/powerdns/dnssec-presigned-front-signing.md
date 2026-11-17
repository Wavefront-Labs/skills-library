---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-presigned-front-signing
name: dnssec-presigned-front-signing
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, presigned, front-signing, opendnssec, secondary, rectify]
level: practitioner
status: docs-checked
description: "Choose between PowerDNS presigned zones and front-signing a secondary: when each applies, NSEC/NSEC3 RRSIG import caveat, and the automatic rectify on retrieval."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/modes-of-operation.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/backends/bind.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Presigned records and front-signing

Pre-signed records:
- Use when the zone already carries DNSSEC records: you are a secondary of an online-signing primary, or the zone was signed with OpenDNSSEC, `ldns-signzone` or `dnssec-signzone`.
- PowerDNS still synthesises NSEC and NSEC3 records itself, so their RRSIGs must be imported too.
- Follow the Presigned migration guide to move such zones.
- On a BIND-backend secondary serving presigned zones, `bind-dnssec-db` must be set or the zone is served silently without DNSSEC.

Front-signing:
- PowerDNS acts as a signing secondary of an unsigned primary.
- If keys exist for the zone they are used when serving it.
- During retrieval the equivalent of `pdnsutil zone rectify` runs automatically (`rectify-zone` before 5.0).

## Checked

2026-11-04. Read the pre-signed and front-signing sections of dnssec/modes-of-operation.rst and the bind-dnssec-db warning in backends/bind.rst; confirmed all claims including the automatic rectify and pre-5.0 name. Nothing removed.

Method: documentation only; no commands were run.
