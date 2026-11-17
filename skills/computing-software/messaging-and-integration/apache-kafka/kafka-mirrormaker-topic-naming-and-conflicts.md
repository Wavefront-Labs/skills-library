---
id: computing-software.messaging-and-integration.apache-kafka.kafka-mirrormaker-topic-naming-and-conflicts
name: kafka-mirrormaker-topic-naming-and-conflicts
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, mirrormaker-2, replication-policy, replication-policy-separator]
level: advanced
status: docs-checked
description: "Control remote topic names with replication.policy.separator and avoid racy MirrorMaker configs against the same target cluster."
sources:
  - https://kafka.apache.org/42/operations/geo-replication-cross-cluster-data-mirroring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand how replicated topics are named and keep MirrorMaker processes consistent.

Naming: remote topics are renamed by a replication policy so records from different clusters never land in the same topic-partition. The default DefaultReplicationPolicy names them `{source}.{source_topic_name}`, so topic foo from cluster us-west becomes us-west.foo on us-east.

Change the separator (default `.`):
`us-west->us-east.replication.policy.separator = _`
For full control, implement a custom ReplicationPolicy and set `replication.policy.class` (default DefaultReplicationPolicy).

Conflicts: MirrorMaker processes share configuration through their target Kafka clusters. Two processes against the same target with different settings are racy. For example, process 1 with `A->B.topics = foo` and process 2 with `A->B.topics = bar`: depending on which process is the elected leader, only foo or only bar is replicated, not both. Keep the configuration consistent for all flows to the same target cluster, for example with automation tooling or one shared MirrorMaker configuration file for the organization.

Config changes take effect only after the MirrorMaker processes are restarted.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 geo-replication page (naming and conflicts sections). All claims matched; no content changes. No hands-on run.
