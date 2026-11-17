---
id: computing-software.networking-hardware-and-wireless.powerdns.soa-edit-signed-zones
name: soa-edit-signed-zones
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, soa-edit, dnssec, rrsig, default-soa-edit, soa-edit-spread, rrsig-expiry-extend]
level: advanced
status: docs-checked
description: "Keep secondaries fresh for PowerDNS-signed zones with SOA-EDIT modes, default-soa-edit and soa-edit-spread."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/dnssec/operational.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOA-EDIT for signed zones

Live signing does not bump the serial when RRSIGs roll (weekly, Thursday 00:00 UTC). PowerDNS secondaries notice changed RRSIGs and re-transfer anyway; non-PowerDNS secondaries need SOA-EDIT, set via `soa-edit` zone metadata or globally with `default-soa-edit` / `default-soa-edit-signed`. The stored serial is untouched; SOA-EDIT affects served SOA answers only.

Modes:
- `INCREMENT-WEEKS`: serial plus weeks since the UNIX epoch. Works everywhere, but not YYYYMMDDSS shaped.
- `INCEPTION-EPOCH`: the larger of the old serial and the last inception time as seconds since the epoch. The backend serial must be epoch seconds.
- `INCEPTION-INCREMENT`: YYYYMMDDSS format; adds 2 if the backend serial is within two days of inception, so keep SS below 98. Uses local time.
- `EPOCH`: serial equals seconds since the epoch. Do not combine with AXFR, or secondaries refresh constantly.
- `NONE`: ignores the `default-soa-edit` settings.

Spreading load (5.1.3+): `soa-edit-spread` spreads serial bumps over N seconds, chosen from a hash of the zone name. Use it with `rrsig-expiry-extend`, which by default extends RRSIG expiry by the same amount so signatures do not expire on secondaries.

Signature validity is three weeks; `rrsig-expiry-extend` can stretch expiry up to a year.

## Checked

2026-11-08. Read in full: PowerDNS docs dnssec/operational.rst (SOA-EDIT section) plus the Signatures section of dnssec/modes-of-operation.rst. Confirmed the weekly Thursday roll, the secondary behaviour, the datastore note, all five modes, the 5.1.3 spread setting, the rrsig-expiry-extend pairing, the three-week validity and the one-year limit. Corrected the INCEPTION-EPOCH description.

Method: documentation only; no commands were run.
