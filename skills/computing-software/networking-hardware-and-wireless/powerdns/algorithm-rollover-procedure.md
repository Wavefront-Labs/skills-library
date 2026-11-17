---
id: computing-software.networking-hardware-and-wireless.powerdns.algorithm-rollover-procedure
name: algorithm-rollover-procedure
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, algorithm-rollover, publish-key, unpublish-key, ecdsa384, pdnsutil]
level: advanced
status: docs-checked
description: "Change a PowerDNS zone's DNSSEC algorithm: add active unpublished KSK and ZSK, publish them, swap the DS, unpublish old DNSKEYs, then deactivate old keys, with waits."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/algoroll.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Algorithm rollover

Assumes a KSK plus ZSK setup (with a CSK, skip the ZSK lines). Bump the serial after every change except the DS update: `pdnsutil zone increase-serial example.com`. Confirm larger responses and TCP work on you and your secondaries.

1. Confirm the current setup and parent DS have been stable a few days.
2. New RRSIGs:
```
pdnsutil zone add-key example.com KSK active unpublished ecdsa384
pdnsutil zone add-key example.com ZSK active unpublished ecdsa384
```
Note the IDs (`pdnsutil zone show example.com`), then wait the highest TTL in the zone (including SOA TTL and SOA MINIMUM).
3. New DNSKEY: `pdnsutil zone publish-key example.com 3` and the same for `4`. Check both old and new keys appear in `dig DNSKEY`. Wait the DNSKEY TTL (from SOA MINIMUM).
4. New DS: take it from `pdnsutil zone show` or `zone export-ds` (both algorithms listed), submit only the new-algorithm DS, remove the old one, confirm it is published, and wait the old DS TTL.
5. Old DNSKEYs: `pdnsutil zone unpublish-key example.com 1` and `2`. Check secondaries; wait the DNSKEY TTL.
6. Old RRSIGs: `pdnsutil zone deactivate-key example.com 1` and `2`, or `zone remove-key` to remove every trace. Old signatures expire from caches in hours to days.

Before 5.0 use `increase-serial` and the `*-zone-key` and `show-zone` names.

## Checked

2026-11-04. Read the whole PowerDNS Algorithm Rollover guide (guides/algoroll.rst) and confirmed every phase, command, wait and the pre-5.0 command names. Nothing removed.

Method: documentation only; no commands were run.
