---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-anti-spyware-and-dns-sinkhole
name: pan-os-anti-spyware-and-dns-sinkhole
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [anti-spyware-profile, pan-os, dns-sinkhole, botnet, threat-prevention, dns-security, c2-detection]
level: practitioner
status: draft
description: "Set up PAN-OS anti-spyware profiles with severity actions and DNS sinkhole to find infected hosts calling command-and-control domains."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/threat-prevention/use-dns-queries-to-identify-infected-hosts-on-the-network"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: block and identify clients beaconing to malicious domains.

```
configure
set profiles spyware AS-STD rules block-high-crit severity [ critical high ] threat-name any category any action block-ip
set profiles spyware AS-STD rules default-alert severity [ medium low informational ] threat-name any category any action default
set profiles spyware AS-STD botnet-domains sinkhole ipv4-address pan-sinkhole-default-ip ipv6-address ::1
set profile-group PG-STANDARD spyware AS-STD
commit
```
DNS sinkhole: the firewall answers malicious domain lookups with a sinkhole IP, so the infected host connects to it (and logs show the host) instead of the attacker. Place the firewall in the DNS path; if clients use an internal resolver, the logs show the resolver IP not the client, so route the traffic log through the resolver or deploy the sinkhole on the resolver's egress and use the sinkhole IP traffic to find clients.

DNS Security (licence) adds cloud DNS categories (malware, C2, DGA, newly registered) that can be sinkholed or blocked per category (confirm names).

Gotchas
- Sinkhole IP must be routable through the firewall so the beacon connection is logged; the default IP is a vendor address that requires egress via the firewall (confirm).
- Reset-both on TCP threats can break poorly behaving apps; use alert first on high-volume rules.

## Verify
```
show log threat direction equal backward
```
Look for threat type `spyware` with category `dns-c2` or sinkhole hits; test a known-safe test domain from the vendor documentation.
