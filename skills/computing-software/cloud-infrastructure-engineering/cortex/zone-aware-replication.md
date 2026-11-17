---
id: computing-software.cloud-infrastructure-engineering.cortex.zone-aware-replication
name: zone-aware-replication
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [zone-awareness, replication, availability-zones, ingesters, store-gateway]
level: advanced
status: docs-checked
description: "Make Cortex replicas span availability zones, with the flags, minimum zone count and balance requirements."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/zone-replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default replicas are spread across the whole instance pool, so all replicas of some data may sit in one zone. Zone-aware replication guarantees replicas land in different zones. Reads survive zone failures as long as no more than `floor(replication factor / 2)` zones have failing instances. It is supported by distributors and ingesters, and by store-gateways (blocks storage).

Enable for ingesters in this order:

1. Set each ingester's zone with `-ingester.availability-zone`.
2. Roll out the ingesters.
3. Set `-distributor.zone-awareness-enabled` on distributors, queriers and rulers.

Constraints: you need at least as many zones as the replication factor (3 zones for RF 3); more is fine, fewer causes missed replica writes and sometimes failed writes. Every zone must run the same number of instances of a zone-aware service, otherwise smaller zones come under higher CPU and memory pressure. Cross-zone network traffic is charged by most cloud providers, so costs rise compared with a single zone.

`-distributor.shard-by-all-labels` affects read availability: when true, a metric is spread over all ingesters, so a large outage across more than one zone fails all queries; when false only RF ingesters hold a metric and some queries may still succeed. Store-gateway zone awareness is configured per the store-gateway documentation, which this skill does not cover.

## Checked

Method: docs-checked 2026-11-09 against the Cortex zone aware replication guide (raw markdown, read in full).
