---
id: computing-software.networking-hardware-and-wireless.check-point.threat-prevention-ips-av-antibot
name: threat-prevention-ips-av-antibot
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, threat-prevention, ips, anti-bot]
level: practitioner
status: draft
description: "Configure Check Point Threat Prevention policy and profiles (IPS, Anti-Virus, Anti-Bot), exceptions and prevent/detect modes."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ThreatPrevention_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat Prevention: IPS, Anti-Virus and Anti-Bot profiles

- Threat Prevention is its own policy and layer (Security Policies > Threat Prevention). Rules choose a **Profile** (Optimized, Strict, Basic, Recommended built-in ones) that sets per-blade protections and confidence/performance filters.
```
mgmt_cli -r true add threat-profile name "Prof_DMZ" active-protections-performance-impact "Medium or lower" active-protections-severity "Medium or above" confidence-level-high "Prevent" confidence-level-medium "Prevent" confidence-level-low "Detect" anti-bot true anti-virus true ips true
mgmt_cli -r true add threat-rule layer "Standard Threat Prevention" position top name "DMZ outbound" protected-scope "net_dmz" action "Prof_DMZ"
mgmt_cli -r true publish
```
- Start new IPS profiles in **Detect**, review logs for a week, then move to **Prevent**; add **Exceptions** (per protection, per rule or global) for false positives instead of switching off the whole blade.
- Protected Scope limits inspection to specific networks; "Any" can drive CPU load.
- Updates: Threat Prevention needs the gateway to pull IPS, AV and Anti-Bot updates from ThreatCloud (Manage & Settings > Updates, or `cpstat -f update_status ...`; confirm). Without it, protections go stale.
- Anti-Bot/AV scanning depends on **HTTPS Inspection** to see TLS traffic (an Anti-Bot DNS check still works with DNS trap).
- Gotcha: the Threat Prevention policy installs separately from Access Control (both in the install dialog).

Verify: test with the EICAR file in a controlled lab or the Check Point test URL; log shows `Protection Name`, `Confidence Level`, `Action: Prevent`. `fw ctl get int ...` is not required; `cpstat blades` shows blade state.
