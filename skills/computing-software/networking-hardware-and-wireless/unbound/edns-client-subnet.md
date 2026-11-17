---
id: computing-software.networking-hardware-and-wireless.unbound.edns-client-subnet
name: edns-client-subnet
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, edns-client-subnet, subnetcache, send-client-subnet, client-subnet-zone, ecs]
level: sme
status: docs-checked
description: "Enable EDNS Client Subnet in Unbound with the subnetcache module: who to send it to, prefix lengths, minimum masks and tree size limits."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# edns client subnet
Needs `subnetcache` in `module-config`, placed just before `iterator`.

- `send-client-subnet`: IP or netblock (`/num`) of servers to send ECS to; repeatable.
- `client-subnet-zone`: domains to send ECS for; repeatable.
- `client-subnet-always-forward` (default no).
- `max-client-subnet-ipv4` (24) and `max-client-subnet-ipv6` (56): longest source prefix.
- `min-client-subnet-ipv4` and `min-client-subnet-ipv6` (default 0): queries with shorter masks get REFUSED.
- `max-ecs-tree-size-ipv4` and `max-ecs-tree-size-ipv6` (100 each).

Counters: `num.query.subnet` (answers containing ECS data) and `num.query.subnet_cache` (answers from the subnet cache, counted as cachemiss in the main counters).

`cache_lookup` also shows matching subnet-cache entries.

## Checked
2026-11-04. Confirmed against the unbound.conf manual: send-client-subnet, client-subnet-zone, client-subnet-always-forward, max/min-client-subnet prefix defaults and max-ecs-tree-size defaults. Nothing removed.
Method: documentation only; no commands were run.
