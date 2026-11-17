---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.streaming-cost-optimisation
name: streaming-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, architecting-for-cost, streaming-cost-optimisation, kafka, messaging-cost]
level: advanced
status: docs-checked
description: "Reduce Kafka streaming cost: cross-AZ traffic and follower fetching (KIP-392), producer compression and batching, per-topic retention and tiered storage."
sources: ["https://cwiki.apache.org/confluence/display/KAFKA/KIP-392%3A+Allow+consumers+to+fetch+from+closest+replica", "https://kafka.apache.org/41/configuration/producer-configs/", "https://kafka.apache.org/41/configuration/topic-configs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messaging and streaming cost (Kafka)

Streaming bills come from brokers (always on), storage (retention times replication) and network.

## Kafka (self-managed or managed)
- **Cross-AZ traffic**: KIP-392 describes the common deployment where each availability zone is
  treated as a datacenter, and notes that before follower fetching consumers could only read from
  the leader, leaving no easy way to use locality to reduce expensive cross-datacenter traffic.
  - **Follower fetching**: set the broker `replica.selector.class` (default `LeaderSelector`, which
    always returns the leader) to a rack-aware selector, set `broker.rack` on brokers to the AZ, and
    set the consumer `client.rack` (default null) to the consumer's AZ.
  - Trade-offs from the KIP: follower fetching may have higher latency, because the high watermark
    propagates through the leader, and consumers can see `OFFSET_NOT_AVAILABLE` and retry.
- **Compression**: the producer `compression.type` defaults to none; valid values are none, gzip,
  snappy, lz4 and zstd. Compression applies to full batches, so batching (`batch.size`, `linger.ms`)
  affects how well it works.
- **Retention**: `retention.ms` and `retention.bytes` are per-topic settings under the delete policy;
  by default there is no size limit, only a time limit. Set them to what consumers actually need.
- **Tiered storage**: the topic setting `remote.storage.enable` (default false) enables remote
  (tiered) storage for a topic.

## Verify
- [ ] Cross-AZ bytes measured before and after follower fetching.
- [ ] Compression type, batching settings and retention documented per topic.

## Checked

Method: docs-checked 2026-11-09 against KIP-392 (cwiki, motivation, follower fetching and public interfaces sections), the Kafka 4.1 producer configs page (compression.type) and topic configs page (retention.ms, retention.bytes, remote.storage.enable).
Removed as unconfirmed: all Kinesis, SQS/SNS, Pub/Sub, Event Hubs and Service Bus content (AWS and Google docs unreadable), the "cross-AZ is often the largest line" claim, replication-factor arithmetic, linger.ms 5-50 and "2-5x" compression figures, the Kinesis price and 25 KB payload unit, and the broker right-sizing advice.
