---
id: computing-software.networking-hardware-and-wireless.bind9.secure-delegation-ds-cds
name: secure-delegation-ds-cds
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, ds-record, cds, cdnskey]
level: practitioner
status: docs-checked
description: "Publish a DS record at the parent for a BIND 9 signed zone: CDS and CDNSKEY automation, dig, and dnssec-dsfromkey."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# secure delegation ds cds
After signing, the parent zone needs a DS record. Options in order of recommendation:

1. Automatic: BIND generates CDS and CDNSKEY records and the parent, registry or registrar updates the DS from them. This needs RFC 7344 support on the parent side.
2. Query the zone for the CDS or CDNSKEY records with `dig`, then submit them by the parent's method (web form, e-mail, API).
3. Generate DS records manually with `dnssec-dsfromkey` and insert them into the parent zone.

`dnssec-dsfromkey -C` outputs CDS records instead of DS. `dnssec-cds` changes DS records at a delegation point based on the CDS or CDNSKEY records published in the child zone; it requires them to be validly signed by a key in the existing DS set. `dnssec-importkey` reads a public DNSKEY record and generates .key and .private files.

## Checked

2026-11-04. Confirmed against the ARM DNSSEC chapter (Secure Delegation) and the dnssec-dsfromkey, dnssec-cds and dnssec-importkey man pages. Removed the unconfirmed claim about validators and an unpublished DS.

Method: documentation only; no commands were run.
