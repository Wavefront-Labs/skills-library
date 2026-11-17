---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-publish-ds-cds
name: dnssec-publish-ds-cds
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, ds, cds, cdnskey, pdnsutil, parent-zone, go-insecure]
level: practitioner
status: docs-checked
description: "Hand a PowerDNS signed zone to its parent: pdnsutil zone show for DS/DNSKEY, CDS and CDNSKEY publication, dnssec-disable, and why the parent DS must go first."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/operational.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing DS, CDS and CDNSKEY

- Show what the parent needs: `pdnsutil zone show ZONE` (`show-zone` before 5.0). Some parents want DS, others DNSKEY; transfer it securely.
- Automate with `pdnsutil zone set-publish-cds ZONE` or `pdnsutil zone set-publish-cdnskey ZONE`; this covers bootstrapping and rollovers.
- Unauthenticated CDS/CDNSKEY bootstrapping is weak: some registries merely wait a few days, which is not authentication.

Going insecure:
```
pdnsutil zone dnssec-disable ZONE
```
(`disable-dnssec` before 5.0.) If the parent still holds a DS record, the zone becomes BOGUS, so have the parent remove the DS first.

TTLs in PowerDNS-signed zones:
- RRSIG TTL equals the covered RRset's TTL.
- CDS, CDNSKEY, DNSKEY, NSEC, NSEC3 and NSEC3PARAM use the SOA minimum.
- NSEC/NSEC3 use the negative TTL (lower of SOA TTL and SOA minimum) per RFC 9077 since 4.3.0.
- For a normal DNSKEY TTL with short negative caching, set the SOA minimum high and the SOA record TTL low; NSEC then carries the high TTL, which may affect aggressive NSEC caching (RFC 8198).

## Checked

2026-11-04. Read dnssec/operational.rst in full and confirmed the manual DS steps, set-publish-cds and set-publish-cdnskey, the bootstrapping authentication caveat, dnssec-disable and the BOGUS warning, and the TTL notes including RFC 9077 behaviour since 4.3.0. Nothing removed.

Method: documentation only; no commands were run.
