---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.route-domains
name: route-domains
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, route-domains, rd, overlapping-ip]
level: practitioner
status: draft
description: "Create BIG-IP route domains with per-RD parent, strict isolation and %id addressing for tenants with overlapping IPs."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Route domains for overlapping address space

Route domains separate routing tables so tenants can reuse the same subnet.
```
tmsh create net route-domain tenantA id 10 vlans add { vlanA } strict enabled
tmsh create net self 10.0.0.5%10/24 vlan vlanA
tmsh create ltm node 10.0.0.20%10
tmsh create ltm virtual vsA destination 10.0.0.100%10:80 pool poolA
tmsh create net route 0.0.0.0/0%10 gw 10.0.0.1%10
```
- The `%id` suffix on an address selects the domain. Without it, the address belongs to the partition's default route domain (0 unless changed per partition: `tmsh modify auth partition X default-route-domain 10`).
- `strict enabled` stops a connection crossing between domains; `strict disabled` allows it only via a `parent-id` relationship.
- Floating or per-domain settings: each domain has its own default route and static routes; use `%id` on the gateway.
- Monitors against `%10` members run in that domain. In iRules, `IP::client_addr` returns the address with the `%id` appended, which breaks `matchclass`/string compares; strip with `[IP::addr [IP::client_addr] mask 255.255.255.255]` or `[string map]`.
- Gotcha: a VLAN can be in only one route domain. Move it first or creation fails.

Verify: `tmsh list net route-domain`, then `ping 10.0.0.1%10` from the BIG-IP shell to prove the domain reaches its gateway.
