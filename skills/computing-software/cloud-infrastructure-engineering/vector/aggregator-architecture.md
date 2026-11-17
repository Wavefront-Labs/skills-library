---
id: computing-software.cloud-infrastructure-engineering.vector.aggregator-architecture
name: aggregator-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [aggregator, architecture, high-availability, load-balancer, disk-buffers, kafka, vector]
level: practitioner
status: docs-checked
description: "Run Vector as dedicated aggregator nodes that receive from agents and own processing and durability."
sources:
  - https://vector.dev/docs/setup/going-to-prod/arch/aggregator/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The aggregator architecture deploys Vector on dedicated nodes for remote processing, ingesting from upstream agents or systems. The docs recommend it for most users, for high availability and easy setup, and it slots into complex environments without changing existing agents.

Architecting:

- Deploy multiple aggregators within each network boundary (each cluster or VPC).
- Use DNS or service discovery to route agent traffic to them.
- Use HTTP-based protocols where possible, and the `vector` source and sink between Vector instances.
- Shift processing and durability to aggregators and keep agents as simple forwarders.

High availability:

- Spread aggregators across nodes and availability zones.
- Enable end-to-end acknowledgements for all sources.
- Use disk buffers on the system-of-record sink and waterfall buffers on the analysis sink.
- Route failed data to the system of record.

Sizing: front aggregators with a load balancer, provision at least 4 vCPUs and 8 GiB per instance, and autoscale on a target of 85% CPU.

Pub-sub: the docs advise against provisioning a new pub-sub service solely for Vector. If you already run Kafka, consume from it, partition by data origin (service or host), use memory buffers with `when_full: block` so backpressure reaches the durable broker, and enable acknowledgements on the `kafka` source.

## Checked

Method: docs-checked 2026-11-09 against the full Vector aggregator architecture page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced load balancer health-check line.
