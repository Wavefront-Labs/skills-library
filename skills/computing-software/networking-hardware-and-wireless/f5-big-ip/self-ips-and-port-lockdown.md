---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.self-ips-and-port-lockdown
name: self-ips-and-port-lockdown
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, self-ip, port-lockdown, allow-service]
level: practitioner
status: draft
description: "Create self IPs, set allow-service port lockdown, and choose floating versus non-floating self IPs on BIG-IP."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self IPs and port lockdown

Self IPs give the BIG-IP an address on a VLAN; non-floating ones are unit-specific, floating ones move with a traffic group.
```
tmsh create net self 10.1.10.245/24 vlan external allow-service default
tmsh create net self float-ext 10.1.10.240/24 vlan external traffic-group traffic-group-1 allow-service none
tmsh modify net self 10.1.10.245 allow-service add { tcp:443 }
tmsh list net self all-properties
```
- `allow-service` is the port lockdown. `default` opens a set including TCP 4353 (config sync/iQuery), UDP 1026 (network failover), TCP 443, TCP 22 and ICMP. `none` blocks everything except what the BIG-IP needs to route. Use `all` only on a management-like VLAN.
- Config sync and failover peers need non-floating self IPs allowing `tcp:4353` and `udp:1026`. Do not point a device group at floating addresses.
- Floating self IPs go in `traffic-group-1`; they are the default gateway for pool members and must not host management services (use `none`).
- Gotcha: a self IP whose network overlaps another VLAN's self IP causes asymmetric ARP and odd reachability. Keep each VLAN on a distinct subnet or isolate in route domains.

Verify: from a peer host `ping`/`curl -k https://selfip`; if lockdown blocks it, it times out while `tmsh show net self` shows the address active. Check `tmsh list net self-allow` for the global defaults (confirm on your version).
