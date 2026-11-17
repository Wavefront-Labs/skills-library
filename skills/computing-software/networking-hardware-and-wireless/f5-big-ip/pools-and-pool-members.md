---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.pools-and-pool-members
name: pools-and-pool-members
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, pools, pool-members, priority-groups]
level: practitioner
status: draft
description: "Create BIG-IP pools with members, ratio, priority groups, minimum-active-members and slow ramp."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pools and pool members

```
tmsh create ltm pool pool_web monitor http load-balancing-mode least-connections-member members add { 10.1.20.11:80 { ratio 3 } 10.1.20.12:80 { priority-group 5 } 10.1.20.13:80 { priority-group 5 } } min-active-members 1 slow-ramp-time 60 service-down-action reselect
tmsh modify ltm pool pool_web members modify { 10.1.20.11:80 { session user-disabled } }
tmsh show ltm pool pool_web members
```
- A pool member is IP:port; the node is the IP only and has its own monitor and state. A node marked down takes all members on that IP down.
- Priority group activation: members in the highest priority group take traffic until fewer than `min-active-members` are available, then the next group joins.
- `slow-ramp-time` (seconds) throttles new connections to a freshly up member (only meaningful with dynamic methods, confirm).
- `service-down-action` values: `none` (existing flows continue), `reset`, `reselect` (move to another member), `drain`.
- Members can be FQDN nodes: `members add { app.example.com:80 { fqdn { autopopulate enabled } } }`.
- Gotcha: a pool monitor and a node monitor are AND-ed; a member needs both to pass. A `min` monitor assignment (`min 2 of { a b }`) is supported with `monitor min 2 of { http tcp }`.

Verify: `tmsh show ltm pool pool_web members` columns Avail, Mon, Enabled; `tmsh show ltm pool pool_web detail` for current connections per member.
