---
id: computing-software.messaging-and-integration.redpanda.consumer-offsets-commit-strategies-and-practices
name: consumer-offsets-commit-strategies-and-practices
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [consumer-offsets, consumer-groups, offset-commit, auto-commit, consumer-offsets-topic, heartbeat]
level: practitioner
status: docs-checked
description: "Pick a Redpanda consumer offset commit strategy, understand the __consumer_offsets topic, and apply best practices on commit frequency, unique groups and heartbeats."
sources:
  - https://docs.redpanda.com/streaming/current/develop/consume-data/consumer-offsets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each message gets an offset in its partition. Consumers commit offsets themselves (Redpanda does not), and the group coordinator appends each OffsetCommitRequest to the compacted `__consumer_offsets` topic, replying only after all replicas of that topic have it.

**Strategies**
- **Automatic** (default): `enable.auto.commit` with a commit every `auto.commit.interval.ms`. Simple, but the consumer does not know what was committed. If it consumes and writes to another datastore and that write fails, auto commit can still advance, causing dropped data.
- **Manual synchronous** (`commitSync`): retries automatically and lets you act before continuing, at the cost of latency. Do not call it after every message.
- **Manual asynchronous** (`commitAsync`): lower latency, no automatic retry, more complex code.
- **External**: set `enable.auto.commit` to false, use `assign(Collection<TopicPartition>)`, save the offset from each ConsumerRecord outside Redpanda, and `seek(TopicPartition, long)` on restart. These consumers do not appear in Redpanda Console group lists (normal for Spark Structured Streaming).
- **Hybrid**: assign partitions directly but commit offsets to Redpanda.

**Best practices**
- Avoid over-committing: every commit is a write to `__consumer_offsets`, and queued async commits are not coalesced by many clients. Monitor commit latency and commit less often if it grows.
- Use a unique consumer group per application. All commits for a group go to one partition of the offsets topic, so reusing a group concentrates the load.
- In highly parallel apps, raise `heartbeat.interval.ms` together with `session.timeout.ms`; 3,200 consumers at 500 ms generate 6,400 heartbeats per second.

## Checked

The strategies, internal topic behaviour and the three best practices were confirmed on the Consumer Offsets page.

Method: docs-checked 2026-11-09 against the Consumer Offsets page, read in full; no commands were run.
