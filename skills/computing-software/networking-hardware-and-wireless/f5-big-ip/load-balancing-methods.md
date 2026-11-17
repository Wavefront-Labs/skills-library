---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.load-balancing-methods
name: load-balancing-methods
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, load-balancing, round-robin, least-connections, ratio]
level: practitioner
status: draft
description: "Pick BIG-IP load balancing methods (round robin, ratio, least connections, observed, predictive, fastest) and their effect."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load balancing methods

```
tmsh modify ltm pool pool_web load-balancing-mode round-robin
tmsh modify ltm pool pool_web load-balancing-mode ratio-member
tmsh modify ltm pool pool_web load-balancing-mode least-connections-member
tmsh modify ltm pool pool_web load-balancing-mode dynamic-ratio-member   # needs performance monitor
```
- Static: `round-robin`, `ratio-member` / `ratio-node` (weights, via `ratio` on member or node), `ratio-session`.
- Dynamic: `least-connections-member` (default for variable-length requests), `least-connections-node`, `observed-member` and `predictive-member` (ranking by connection counts over time), `fastest-app-response` (uses response times), `dynamic-ratio` (uses SNMP/WMI performance data).
- Least connections counts layer 4 connections, not requests; with OneConnect or HTTP/2 reuse it can balance poorly. Combine with `slow-ramp-time` so a recovered node is not flooded.
- Ratio methods ignore live load. Setting `ratio 0` effectively stops new traffic without disabling the member.
- Node methods (`-node`) consider all connections to that IP across pools, member methods only that pool.
- Persistence overrides the method for returning clients; only the first request is balanced.
- Gotcha: after changing the method, existing persistence records keep old mappings; new rules apply only to new sessions.

Verify: send 100 requests (`for i in $(seq 100); do curl -s http://vip/id; done | sort | uniq -c`) and compare per-member counters in `tmsh show ltm pool pool_web members`.
