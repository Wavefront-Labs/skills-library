---
id: computing-software.networking-hardware-and-wireless.powerdns.zsk-rollover-procedure
name: zsk-rollover-procedure
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, dnssec, zsk, key-rollover, pdnsutil, add-key, activate-key]
level: practitioner
status: docs-checked
description: "Roll a PowerDNS ZSK in order: add inactive published key, activate new, deactivate old, remove old, with the waits."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/zskroll.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZSK rollover

Pre-check: run `pdnsutil zone show example.com` (`show-zone` before 5.0) to confirm the key is not a SEP and note its algorithm. Bump the serial after each change.

1. Let the old ZSK sign for a few days or longer.
2. Publish the new key:
   `pdnsutil zone add-key example.com zsk inactive published ALGORITHM`
   Note its ID, check `dig DNSKEY example.com @...` on the secondaries shows both keys, and wait at least the DNSKEY TTL.
3. Switch signatures:
   `pdnsutil zone activate-key example.com NEW-ZSK-ID`
   `pdnsutil zone deactivate-key example.com OLD-ZSK-ID`
   Check secondaries serve only new signatures, then wait at least the highest TTL in the zone, including SOA TTL and SOA MINIMUM (the DNSKEY TTL also comes from SOA MINIMUM).
4. Remove the old key:
   `pdnsutil zone remove-key example.com OLD-ZSK-ID`
   Check only the new DNSKEY remains, and wait one more DNSKEY TTL.

Legacy command names before 5.0: `add-zone-key`, `activate-zone-key`, `deactivate-zone-key`, `remove-zone-key`. Check the zone with DNSViz, the VeriSign DNSSEC Analyzer, or a validating resolver after every change.

## Checked

2026-11-08. Read in full: PowerDNS docs guides/zskroll.rst. Confirmed the pre-publish phases, each pdnsutil command and its pre-5.0 name, the SEP and algorithm pre-check, the serial bump, the TTL waits (DNSKEY TTL, then highest zone TTL including SOA TTL and SOA MINIMUM, then one more DNSKEY TTL) and the named checkers. Nothing removed.

Method: documentation only; no commands were run.
