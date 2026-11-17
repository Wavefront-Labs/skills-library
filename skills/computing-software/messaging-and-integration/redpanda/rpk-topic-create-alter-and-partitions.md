---
id: computing-software.messaging-and-integration.redpanda.rpk-topic-create-alter-and-partitions
name: rpk-topic-create-alter-and-partitions
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rpk, topic, create, alter-config, add-partitions, replication-factor, dry-run]
level: practitioner
status: docs-checked
description: "Create topics, change their configuration incrementally and add partitions with rpk topic create, alter-config and add-partitions, including replication rules and dry runs."
sources:
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-topic/rpk-topic-create/
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-topic/rpk-topic-alter-config/
  - https://docs.redpanda.com/streaming/current/reference/rpk/rpk-topic/rpk-topic-add-partitions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Create.** One invocation applies the same partitions, replicas and configs to every topic named:

```bash
rpk topic create -c cleanup.policy=compact -r 3 -p 20 topic-1 topic-2
```

Flags: `-p` partitions (-1 uses the cluster `default_topic_partitions`), `-r` replication factor (-1 uses `default_topic_replications`), `-c key=value` repeatable, `-d/--dry` validates without creating, `--if-not-exists`. The replication factor must be a positive odd number no greater than the number of available brokers. From v25.3, properties such as `retention.ms`, `retention.bytes` and `segment.ms` distinguish zero (immediately eligible for cleanup or compaction) from negative (feature disabled).

**Alter config.** Four incremental operations: set a key, delete a key's value, append to a list-valued key, subtract from one.

```bash
rpk topic alter-config <topics...> --set key=value --delete key2,key3
```

Flags: `-s/--set`, `-d/--delete`, `--append`, `--subtract` (all repeatable), `--dry` (validate only), `--no-confirm`, and `-r/--regex` (new in v26.2.2) to treat names as regular expressions over non-internal topics. `rpk topic list` takes the same regex form, so preview the match first.

**Add partitions**
```bash
rpk topic add-partitions <topics...> --num [#]
```
`--num` is the number to add per topic. Existing data is not redistributed to the new partitions. `--force` allows changing internal topics such as `__consumer_offsets`.

Raising replication factor on existing topics uses `rpk topic alter-config <topic-names> --set replication.factor=3`, as in the production deployment page.

## Checked

2026-11-04. Commands, flags, version notes and the odd replication rule were confirmed on the rpk topic create, alter-config and add-partitions pages. The replication.factor command is from the Deploy for Production page.

Method: documentation only; no commands were run.
