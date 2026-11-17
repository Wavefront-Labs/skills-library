---
id: computing-software.cloud-infrastructure-engineering.vector.high-availability-failure-modes
name: high-availability-failure-modes
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [high-availability, failure-modes, disk-failure, node-failure, availability-zones, acknowledgements, vector]
level: advanced
status: docs-checked
description: "Map each Vector failure mode to the mitigation the docs recommend."
sources:
  - https://vector.dev/docs/setup/going-to-prod/high-availability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Understand failure modes before designing for availability.

- **Disk failure** is treated as process failure: Vector fails to start without its disk at boot and exits if it vanishes at runtime. A disk is only needed for components such as disk buffers or the `file` source and sink.
- **Node failure:** distribute Vector and its load balancer over several nodes, fail over on unreachable nodes, keep spare capacity, and use automated self-healing. Rule of thumb: no single node should process more than 33% of data.
- **Data center failure:** deploy across availability zones with enough capacity to lose any one.
- **Process failure:** load balancer failover plus a platform supervisor, such as a Kubernetes controller, restarting the process.
- **Data receive failure:** end-to-end acknowledgements, so Vector answers clients only when data is durably persisted. Pair with disk buffers or streaming sinks so acknowledgements are timely.
- **Data processing failure:** dropped-event routing (see remap-dropped-event-routing).
- **Data send failure:** Adaptive Request Concurrency to avoid stampedes, and buffers to absorb backpressure and replay on recovery.
- **Total system failure:** advanced; fail over to intra-network standbys via service discovery or DNS, keeping standbys in the same network.

Strategy summary: contain the blast radius per network boundary, acknowledge at sources, buffer sinks with disk (or memory that overflows to disk), and route transform failures to your system of record.

Disaster recovery: Vector is shared-nothing and holds no replicated state, so rebuild it at the DR site with the rest of the stack.

## Checked

Method: docs-checked 2026-11-09 against the full Vector high-availability page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced failure-test line.
