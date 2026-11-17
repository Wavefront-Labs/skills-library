---
id: computing-software.networking-hardware-and-wireless.powerdns.svcb-autohints
name: svcb-autohints
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, svcb, https-record, svc-autohints, ipv4hint, ipv6hint, pdnsutil-check]
level: practitioner
status: docs-checked
description: "Auto-fill ipv4hint and ipv6hint in SVCB/HTTPS records with PowerDNS svc-autohints: auto placeholder, drop rules, zone check."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/svcb.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SVCB autohints

Setting: `svc-autohints=yes` (added in 4.5.0).

- Put `ipv4hint=auto` or `ipv6hint=auto` in an SVCB or derived record such as HTTPS. PowerDNS fills them from the A and AAAA records already in the zone, in answers and in AXFR. The literal `auto` is never put on the wire.
- Alias-form records whose target is in the zone get the target's HTTPS and address records added to the additional section.
- If the target has no AAAA records, `ipv6hint` is dropped from the answer and AXFR (the page shows only this IPv6 case).
- With the setting off, any parameter valued `auto` is dropped.

Check a zone:
```
pdnsutil zone check example.com
```
(`check-zone` before 5.0.) It warns when autohints are present but the target lacks matching address records.

## Checked

2026-11-08. Read in full: PowerDNS docs guides/svcb.rst. Confirmed the 4.5.0 version note, autohint filling for answers and AXFR, never serving the literal auto, the additional-section processing, the drop rules, and the zone check warning and its pre-5.0 name. Removed the claim about a new settings style and the claim of no error; generalised IPv4 drop was reworded to what the page shows.

Method: documentation only; no commands were run.
