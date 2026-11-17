---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-external-dynamic-lists
name: pan-os-external-dynamic-lists
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [external-dynamic-list, pan-os, edl, threat-feed, ip-list, url-list, domain-list, refresh]
level: practitioner
status: draft
description: "Consume IP, URL and domain feeds with PAN-OS external dynamic lists, set refresh, authentication and limits, and force a refresh."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/policy/use-an-external-dynamic-list-in-policy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: block or allow lists maintained outside the firewall (threat feeds, partner ranges, SaaS endpoints).

```
configure
set external-list EDL-BLOCK-IPS type ip url https://lists.example.com/block-ips.txt recurring hourly description "internal threat feed"
set rulebase security rules block-edl from any to any source EDL-BLOCK-IPS destination any application any service any action deny log-end yes
commit
```
Types: ip, domain, url, predefined-ip, imsi, imei. Format is plain text, one entry per line, `#` comments.

Operations:
```
request system external-list refresh name EDL-BLOCK-IPS
request system external-list show type ip name EDL-BLOCK-IPS
```
Use certificate profiles to validate HTTPS feeds, and basic auth fields (username/password) when needed. Place the list on a web server reachable through the management or service route.

Gotchas
- Each model has a maximum entries per list and in total; oversize lists are truncated with a system log warning.
- An unreachable server keeps the last good copy (confirm retention) and continues enforcing it; the list does not clear itself.
- Domain EDLs are used in URL category or DNS Security, not directly in security rules (as of recent releases, confirm).

## Verify
```
request system external-list show type ip name EDL-BLOCK-IPS
```
Entries are listed with a recent fetch time; the system log has an "EDL refresh" success entry.
