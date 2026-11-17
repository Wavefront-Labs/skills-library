---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-zone-protection-and-dos-protection
name: pan-os-zone-protection-and-dos-protection
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [zone-protection, pan-os, dos-protection, syn-flood, reconnaissance-protection, packet-based-attack-protection, syn-cookies]
level: practitioner
status: draft
description: "Apply PAN-OS zone protection profiles and DoS protection policies for floods, reconnaissance and malformed packets, and monitor drops."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/zone-protection-and-dos-protection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: protect the firewall and downstream hosts from floods and scans at the edge.

```
configure
set network profiles zone-protection-profile ZP-EDGE flood tcp-syn enable yes
set network profiles zone-protection-profile ZP-EDGE flood tcp-syn syn-cookies alarm-rate 10000 activate-rate 10000 maximal-rate 40000
set network profiles zone-protection-profile ZP-EDGE scan 8001 action block-ip track-by source duration 300
set network profiles zone-protection-profile ZP-EDGE discard-ip-spoof yes
set zone untrust network zone-protection-profile ZP-EDGE
commit
```
Zone protection works per ingress zone and is aggregate (not per source). For per-source or per-destination limits, create a DoS Protection profile (classified, with `session` or `aggregate` type) and a DoS Protection policy rule.

Tuning method: measure normal peak rates from `show session info`, set activate rates at about 2 times peak, alarm at about 1.5 times, and use SYN cookies instead of random early drop where possible.

Gotchas
- Aggressive reconnaissance blocking can block legitimate monitoring scanners; add them to the exclusion list.
- Do not enable flood protection on internal zones with legacy chatty devices without baselining.
- SYN cookies add CPU on dataplane.

## Verify
```
show zone-protection zone untrust
show counter global filter category flow delta yes
show dos-protection zone untrust statistics
```
Drops from flood or scan show in the counters; the threat log shows `flood` and `scan` events (confirm log fields).
