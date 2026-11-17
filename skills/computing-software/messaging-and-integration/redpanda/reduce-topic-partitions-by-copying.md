---
id: computing-software.messaging-and-integration.redpanda.reduce-topic-partitions-by-copying
name: reduce-topic-partitions-by-copying
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [partitions, redpanda-connect, rpk-group, topic-migration, duplicates, ordering]
level: practitioner
status: docs-checked
description: "Partitions cannot be reduced in place. Copy a topic to one with fewer partitions with Redpanda Connect, verify lag and counts, know the caveats."
sources:
  - https://docs.redpanda.com/streaming/current/develop/manage-topics/config-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Kafka API cannot reduce partitions. To move data to fewer partitions, copy it to a new topic.

**Check first**
- Duplicates: Redpanda Connect delivers at least once, so retries can duplicate records.
- Ordering: keys are preserved, so each key stays ordered, but global order across partitions is not.
- Retention: the copy starts at the oldest retained record; finish well within retention.
- Consumer offsets are per topic and do not carry over; use `rpk group seek` to set them.
- Producers must stop writing to the original topic before cutover.

**Steps** (example: `orders`, 3 partitions to 1)
1. `rpk topic describe orders`: note replicas and every row whose SOURCE is `DYNAMIC_TOPIC_CONFIG`; a new topic without those overrides silently falls back to cluster defaults.
2. Create the target:
```bash
rpk topic create orders-reduced --partitions 1 --replicas 1 --topic-config retention.ms=604800000
```
3. Run the pipeline with `rpk connect run reduce-partitions.yaml`:
```yaml
input:
  redpanda:
    seed_brokers: ["<broker-address>"]
    topics: ["orders"]
    consumer_group: orders-to-orders-reduced
    start_offset: earliest
output:
  redpanda:
    seed_brokers: ["<broker-address>"]
    topic: orders-reduced
    key: ${! @kafka_key }
```
Use a consumer group name unique to this copy: `start_offset: earliest` only applies when the group has no committed offset.
4. Stop producers, keep the pipeline running, and wait until `rpk group describe orders-to-orders-reduced` shows LAG 0 on every partition.
5. Compare record counts: per topic, sum of HIGH-WATERMARK minus LOG-START-OFFSET from `rpk topic describe <topic> -p`. A larger count on the new topic means duplicates.
6. Switch clients, stop the pipeline, and only then delete the old topic.

## Checked

2026-11-08. Read the whole Manage Topics page. Confirmed: partitions cannot be reduced, the five caveats (duplicates, ordering, retention, consumer offsets, write downtime), the orders example steps, rpk topic describe and create commands, pipeline YAML, unique consumer group note, rpk group describe lag check, record count comparison, delete last. Nothing removed.

Method: documentation only; no commands were run.
