---
id: computing-software.cybersecurity-defensive.zeek.cluster-node-roles
name: cluster-node-roles
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, cluster-architecture, manager, logger, proxy, worker]
level: practitioner
status: docs-checked
description: "Zeek cluster roles: tap, frontend, manager, logger, proxy and worker, what each does and sizing advice for workers per core."
sources: ["https://docs.zeek.org/en/current/cluster-setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cluster node roles

Zeek is not multithreaded, so scaling means spreading load across cores or machines.

- **Tap**: splits the packet stream, for example a switch monitor port or optical splitter.
- **Frontend**: hardware or on-host technique that splits traffic into flows. The Zeek binary does not do this.
- **Manager**: receives logs and notices from the other nodes, producing one log instead of many, and hosts analysis needing a global view.
- **Logger**: optional. Receives logs instead of the manager to reduce manager load.
- **Proxy**: offloads data storage or arbitrary workload; default scripts use it minimally. Often co-located with the manager.
- **Worker**: sniffs traffic and does protocol analysis. Most work happens here, so buy the fastest memory and cores. Workers need no special disks since logging is remote.

Guidance: run workers on different machines from the manager. Run at most one or two fewer workers than CPU cores. Define a logger to relieve the manager. Combine a load-balancing method such as PF_RING with CPU pinning to cut worker load.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
