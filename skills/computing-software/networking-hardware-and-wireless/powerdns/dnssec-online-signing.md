---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-online-signing
name: dnssec-online-signing
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, online-signing, zsk-rollover, rrsig, hidden-primary, performance]
level: practitioner
status: docs-checked
description: "Operate PowerDNS online DNSSEC signing: shared SQL key store, RRSIG validity and rollover day, ZSK count and rollover order, ALIAS limit, security and performance."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/modes-of-operation.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/operational.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online signing

- One SQL database holds zone data, keys and DNSSEC settings in separate tables; replicate it to every instance over a secure network or encrypted link, since stolen keys let an attacker forge DNSSEC data.
- RRSIGs are computed on the fly and heavily cached, using all CPU cores. They are valid for 3 weeks and roll on Thursdays at 00:00 UTC; one RRSIG per RRset per ZSK is served.
- DNSKEY and NSEC3PARAM TTLs come from the SOA minimum.
- `rrsig-expiry-extend` extends expiry up to one year.
- ZSKs: usually 1, at most 2, one active at a time. Rollover: activate the new key (both active), deactivate the old one, then remove it.
- NSEC mode needs the backend to supply previous and next names in canonical order; NSEC3 inclusive needs hashed ones.
- ALIAS records are not supported in this mode.

Security: private keys stay on the server. To limit exposure use pre-signed mode, or a hidden primary in online mode on a locked-down network, with internet-facing secondaries transferring presigned zones by AXFR.

Performance: the main cost is memory for signature caches. Startup and serving AXFR trigger heavy signing. See RFC 6781 for practice.

## Checked

2026-11-04. Read dnssec/modes-of-operation.rst and dnssec/operational.rst (Security and Performance sections) and confirmed the shared SQL store, replication-security warning, RRSIG 3-week validity with Thursday roll, one RRSIG per ZSK, TTLs from SOA minimum, rrsig-expiry-extend up to a year, ZSK counts and rollover, NSEC and NSEC3 backend needs, the ALIAS limit and the hidden-primary advice. Nothing removed.

Method: documentation only; no commands were run.
