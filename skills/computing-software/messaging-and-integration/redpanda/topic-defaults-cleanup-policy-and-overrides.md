---
id: computing-software.messaging-and-integration.redpanda.topic-defaults-cleanup-policy-and-overrides
name: topic-defaults-cleanup-policy-and-overrides
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [topics, cleanup-policy, topic-properties, defaults, overrides, rpk-topic-describe]
level: practitioner
status: docs-checked
description: "Know which cluster properties supply each topic default, choose partitions and replication, change cleanup.policy, remove overrides and list effective topic configuration."
sources:
  - https://docs.redpanda.com/streaming/current/develop/manage-topics/config-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
New topics take cluster defaults unless you override them. The page maps them:

| Cluster property | Default | Topic property |
|---|---|---|
| `log_cleanup_policy` | delete | `cleanup.policy` |
| `retention_bytes` | null (no limit) | `retention.bytes` |
| `log_retention_ms` | 604800000 (1 week) | `retention.ms` |
| `log_segment_ms` | 1209600000 (2 weeks) | `segment.ms` |
| `log_segment_size` | 134217728 (128 MiB) | `segment.bytes` |
| `log_compression_type` | producer | `compression.type` |
| `log_message_timestamp_type` | CreateTime | `message.timestamp.type` |
| `kafka_batch_max_bytes` | 1048576 | `max.message.bytes` |
| `write_caching_default` | false | `write.caching` |

These defaults suit a one-broker development cluster. Default partitions and replicas are 1; the page recommends replication factor 3 (odd only), and `minimum_topic_replications` sets a cluster floor. A rule of thumb for partitions: match the maximum number of consumers in any consumer group, for example `rpk topic create xyz -p 10`.

**Cleanup policy:** `delete` (by age or size), `compact` (latest value per key) or `compact,delete`.

```bash
rpk topic alter-config [TOPICS…] --set cleanup.policy=compact
```

Properties take effect immediately. Do not modify internal topics such as `__consumer_offsets` or `_schemas`; the page warns it can destabilize the cluster.

**Remove an override** so the default applies again:

```bash
rpk topic alter-config [TOPICS...] --delete cleanup.policy
```

**Inspect:** `rpk topic describe <topic-name> -c` limits output to configs. In `rpk topic describe` the SOURCE column shows `DEFAULT_CONFIG` or `DYNAMIC_TOPIC_CONFIG` (an override).

## Checked

2026-11-04. The default mapping table, partition and replication advice, cleanup policies, warning and the commands were confirmed on the Manage Topics page.

Method: documentation only; no commands were run.
