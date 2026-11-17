---
id: computing-software.messaging-and-integration.redpanda.decide-minimum-broker-count-before-scaling-down
name: decide-minimum-broker-count-before-scaling-down
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [decommission, capacity-planning, replication-factor, racks, retention, logdirs, partitions]
level: advanced
status: docs-checked
description: "Work out how many Redpanda brokers to keep before decommissioning: racks, per-broker disk, replication factor and partitions per core."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/decommission-brokers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before shrinking a cluster, test five constraints and take the strictest.

- **Availability:** `rpk cluster config get enable_rack_awareness` then `rpk cluster info` to list racks. The example shows racks A to D, so at least four brokers to use all racks.
- **Storage:** `rpk cluster logdirs describe --aggregate-into broker` shows bytes used per broker (about 240 GB each over seven brokers, so five brokers need at least 337 GB each for current data). Add retention: throughput x retention x 1.1 padding, divided by target broker count. At 200 MB/sec, 6 hours with five brokers is 4.752 TB / 5, about 950 GB each. The example keeps 6 hours locally with older data in Tiered Storage, giving about 1.2 TB per broker. The 1.1 factor pads for hot spots; raise it if you expect more.
- **Durability:** the cluster needs a quorum (minimum three brokers) and at least as many brokers as the highest topic replication factor. Find it with:
```bash
rpk topic list | tail -n +2 | awk '{print $3}' | sort -n | tail -1
```
A result of 5 means five brokers minimum.
- **Partition count:** total from `curl -sk http://<broker-url>:<admin-api-port>/v1/partitions/local_summary | jq .count` (3018 in the example), against cores from `rpk cluster info -b --detailed`. Eight cores on five brokers gives 40 cores, supporting 40K partitions at 1K per core.
- **Cost:** each broker is an instance; fewer brokers cost less.

The worked example concludes that the replication factor of five is the limiting factor. The page cautions that constant throughput and perfect balance are assumptions.

## Checked

2026-11-08. Read the whole Decommission Brokers page and confirmed all five assessment sections (availability, cost, data retention, durability, partition count), the commands, and the worked numbers (about 240 GB per broker, 337 GB for five brokers, 4.752 TB / 5 = 950.4 GB, about 1.2 TB per broker, 3018 partitions, 40 cores, replication factor 5). The page's own text says padding is 1% while its formulas multiply by 1.1; the skill follows the formulas. The 1K partitions per core figure is derived from 40K partitions on 40 cores in the example.

Method: documentation only; no commands were run.
