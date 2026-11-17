---
id: computing-software.networking-hardware-and-wireless.powerdns.ksk-rollover-procedure
name: ksk-rollover-procedure
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, ksk, key-rollover, export-ds, double-ds, pdnsutil]
level: practitioner
status: docs-checked
description: "Roll a PowerDNS KSK: add the new active published KSK, wait a DNSKEY TTL, export the DS and swap it at the parent, wait the old DS TTL, then remove the old key."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/kskroll.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KSK rollover

Read RFC 6781 section 4 first, and bump the serial after each zone change.

1. Confirm the KSK is active and its DS is at the parent.
2. Add the new key:
   `pdnsutil zone show example.com` (note the algorithm), then
   `pdnsutil zone add-key example.com ksk active published ALGORITHM`
   Note the new ID. Check `dig DNSKEY example.com @<secondary>` shows both keys, then wait at least the DNSKEY TTL.
3. Change the DS:
   `pdnsutil zone export-ds example.com`
   The output lists both KSKs; use only the new one. Check the old DS TTL at the parent (for example `dig DS example.com @c.gtld-servers.net`), submit the new DS (or DNSKEY, per the parent), remove the old one, confirm it is published, then wait at least the old DS TTL.
4. Remove the old key:
   `pdnsutil zone remove-key example.com OLD_KSK_ID`
   Check only the new key is served.
5. Wait at least another DNSKEY TTL; the rollover is complete.

Before 5.0 the commands are `show-zone`, `add-zone-key`, `export-zone-ds`, `remove-zone-key`.

## Checked

2026-11-04. Read guides/kskroll.rst in full and confirmed the phases, commands, waits and pre-5.0 command names. Nothing removed.

Method: documentation only; no commands were run.
