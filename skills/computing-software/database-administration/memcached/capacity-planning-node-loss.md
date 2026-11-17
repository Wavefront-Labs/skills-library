---
id: computing-software.database-administration.memcached.capacity-planning-node-loss
name: capacity-planning-node-loss
category: computing-software
field: database-administration
product: memcached
tags: [capacity-planning, node-loss, hit-rate, failure-domain, cluster-sizing]
level: advanced
status: docs-checked
description: "Plan capacity so losing memcached nodes does not overwhelm the backend: model the hit-rate drop per node lost."
sources:
  - https://docs.memcached.org/serverguide/hardware/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Rule from the Hardware page: get an idea how many servers can be lost before your application is overwhelmed, and make sure you always have more than that. If you cannot take down memcached instances, upgrades (hardware or software) and normal failures are excessively painful.

Worked example from the docs: a 90% hit rate across 10 memcached servers; one dies and the hit rate may drop to 82% or so. Misses rising from 10% to 18-20% means the backend suddenly handles about twice as many requests. Actual impact varies, since databases are decent at repeat queries and many misses would need a lookup anyway. If you can only afford four servers of 144G, losing one removes 25% of the cache and the hit rate can tank even harder.

Practice:
- Keep nodes roughly the same size: cluster uniformity means you can add and remove servers without caring about a particular server's weight, or one hurting more if lost.
- The more you compress the cluster onto fewer hosts, the more pain when a host dies; spreading memory thinly (for example spare memory on webservers) makes losing one less painful, at the cost of extra maintenance and watching multi-get usage, which can touch every server.
- Multiget spreads over more servers as the cluster grows (the multiget hole); grouping related keys on one instance, where the client supports it, reduces the syscalls.
- Hardware gets cheaper: in theory you can halve your server count every few years.

## Checked

2026-11-04. Confirmed against the Hardware and Instances page (capacity planning, 90%/82% example, 144G example, uniformity) and the Performance page (multiget hole, Moore's law). Removed: the miss-rate formula, the "drain a node in staging" test and the unstated blast-radius wording.

Method: documentation only; no commands were run.
