---
id: computing-software.networking-hardware-and-wireless.powerdns.ksk-rollover-cds
name: ksk-rollover-cds
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, ksk, cds, rfc7344, key-rollover, set-publish-cds]
level: practitioner
status: docs-checked
description: "Roll a PowerDNS KSK using CDS records (RFC 7344): add an inactive KSK, publish CDS, wait for the parent, switch keys, remove the old key."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/kskrollcdnskey.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KSK rollover with CDS

1. Add the new KSK inactive, so it signs no ZSK records:
   `pdnsutil zone add-key example.com ksk 2048 inactive`
2. Publish CDS: `pdnsutil zone set-publish-cds example.com`
3. Wait until the parent has updated its DS records.
4. Switch keys (IDs from `pdnsutil zone show example.com`):
   `pdnsutil zone activate-key example.com new-key-id`
   `pdnsutil zone deactivate-key example.com old-key-id`
5. Wait at least the DNSKEY TTL, so validating resolvers do not mark the zone BOGUS.
6. Remove the old key, which makes CDS list only the new key:
   `pdnsutil zone remove-key example.com old-key-id`
7. Wait for the parent to pick up the CDS change; confirm upstream DS shows only the new KSK's DS.
8. Stop publishing: `pdnsutil zone unset-publish-cds example.com`

Before 5.0 the commands are `add-zone-key`, `set-publish-cds`, `activate-zone-key`, `deactivate-zone-key`, `remove-zone-key`, `unset-publish-cds` and `show-zone`. The page shows CDS commands only, not CDNSKEY ones.

## Checked

2026-11-08. Read docs/guides/kskrollcdnskey.rst in full. Confirmed every step, the pdnsutil zone command forms and their pre-5.0 names, the DNSKEY TTL wait and the CDS clean-up. Description shortened. Nothing removed.

Method: documentation only; no commands were run.
