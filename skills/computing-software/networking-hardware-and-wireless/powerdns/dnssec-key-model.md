---
id: computing-software.networking-hardware-and-wireless.powerdns.dnssec-key-model
name: dnssec-key-model
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, ksk, zsk, ds, nsec, nsec3, denial-of-existence]
level: intro
status: docs-checked
description: "Understand PowerDNS DNSSEC basics: KSK versus ZSK, DNSKEY, RRSIG and DS records, authenticated denial with NSEC, NSEC3 inclusive and narrow, and signing advice."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/intro.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/advice.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC key model

- DNSSEC keys are asymmetric (the docs list RSA, DSA, ECDSA, GOST). The public half is published as DNSKEY; the private half signs and is never published. Signatures are RRSIG records.
- Typical layout: a Key Signing Key (KSK) signs the Zone Signing Keys (ZSKs). The KSK is referenced from the parent, so ZSKs can be rotated without telling the parent.
- The parent needs a DS record (a hash of the DNSKEY) before the signed zone is operational.
- Empty answers cannot be signed, so denial is proved with records: NSEC covers the gap between two existing names (and so reveals which names exist); NSEC3 proves no name hashes between two bounds, using an iterated salted hash.
- PowerDNS zone modes: NSEC, NSEC3 inclusive, NSEC3 narrow.

Advice:
- Sign with `pdnsutil zone secure` (`secure-zone` before 5.0) and stick to its default keying.
- Avoid provisioning many or unnecessarily large keys; bigger answers worsen network problems. Mixed algorithms in one zone work but have proven unreliable.
- On a primary with non-PowerDNS secondaries, you may need to adjust the SOA-EDIT metadata.
- The network must pass UDP above 512 bytes on port 53, fragmented UDP, ICMP fragmentation messages, TCP port 53 and EDNS0, or DNSSEC can degrade or break.

## Checked

2026-11-04. Read dnssec/intro.rst and dnssec/advice.rst in full and confirmed the key types, DNSKEY/RRSIG/DS roles, KSK and ZSK purpose, NSEC and NSEC3 explanations, three zone modes, default-keying advice, mixed-algorithm warning, SOA-EDIT hint and the network requirements list. Nothing removed.

Method: documentation only; no commands were run.
