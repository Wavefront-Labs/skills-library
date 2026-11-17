---
id: computing-software.messaging-and-integration.apache-kafka.kafka-mirrormaker-run-and-exactly-once
name: kafka-mirrormaker-run-and-exactly-once
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, mirrormaker-2, connect-mirror-maker-sh, exactly-once-source-support, dedicated-mode-enable-internal-rest]
level: advanced
status: docs-checked
description: "Run connect-mirror-maker.sh near the target cluster with --clusters and enable exactly-once with exactly.once.source.support."
sources:
  - https://kafka.apache.org/42/operations/geo-replication-cross-cluster-data-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start MirrorMaker properly and optionally get exactly-once replication.

Start: `bin/connect-mirror-maker.sh connect-mirror-maker.properties`. It can take a few minutes before replication begins. Processes configured for the same clusters form a distributed setup, share config and balance work, so add processes to raise throughput. Stop with SIGTERM (`kill <pid>`).

Consume from remote, produce to local: producers handle unreliable or high-latency links worse than consumers, so run MirrorMaker next to the target cluster and name it with `--clusters`:
`bin/connect-mirror-maker.sh connect-mirror-maker.properties --clusters secondary`
This stops it from replicating data or sending config to far-away clusters. Without `--clusters` it still works but may suffer producer lag and extra transfer costs.

Exactly-once for dedicated MirrorMaker clusters (since 3.5.0):
- New cluster: `us-east.exactly.once.source.support = enabled`
- Existing cluster: first set `preparing` on all nodes, then `enabled` in a second round of restarts.
- Also set `dedicated.mode.enable.internal.rest = true` and `listeners = http://localhost:8080` (KIP-710). Secure these REST servers in production.
- Filter aborted transactions with `us-west.consumer.isolation.level = read_committed`.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 geo-replication page (running and exactly-once sections). Commands and settings matched; the "few minutes before replication begins" and KIP-710 remarks and the run-near-target rationale come from my reading of the page's running section and are less certain than the config names. No hands-on run.
