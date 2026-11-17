---
id: computing-software.messaging-and-integration.apache-pulsar.topic-compaction
name: topic-compaction
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [topic-compaction, read-compacted, compaction-threshold, compact-topic, compaction-horizon, null-key]
level: practitioner
status: docs-checked
description: "Compact a keyed Pulsar topic to the latest value per key: automatic threshold, manual compaction commands, readCompacted consumers and null-key retention."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-compaction.md
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-topic-compaction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give consumers a shallow, latest-value-per-key view of a topic for fast rewinds without losing the full log.

How it works: compaction iterates the topic once to record the latest occurrence of each key, then writes a new BookKeeper ledger containing only those latest messages (payload, message ID, metadata). A message with an empty payload is skipped and treated as deleted (a tombstone). When done, the ledger ID and the message ID of the last compacted message (the compaction horizon) are stored in topic metadata. Readers with read-compacted enabled read from the horizon for older positions and normally for newer ones. The original topic is left unchanged, so other consumers can still read full history. Compaction applies only to persistent topics, respects retention, and is distinct from retention and expiry.

Requirements: messages need keys; messages without keys are ignored by compaction. Since 3.2.0 the default is not to retain null-key messages; broker setting `topicCompactionRetainNullKey` (PIP-318) controls this (the concepts page calls the setting `compactionRetainNullKey`, so check the name in your broker.conf). Consumers must set `readCompacted(true)` (Java), otherwise they read the non-compacted topic.

Automatic trigger (namespace backlog threshold):
```bash
bin/pulsar-admin namespaces set-compaction-threshold --threshold 100M my-tenant/my-namespace
```
Manual trigger:
```bash
bin/pulsar-admin topics compact persistent://my-tenant/my-namespace/my-topic
bin/pulsar compact-topic --topic persistent://my-tenant/my-namespace/my-topic
```
The second form runs compaction in its own process instead of through the REST API, which is recommended to avoid disturbing broker performance.

Gotcha: after cursor recovery references a compacted ledger deleted by a later compaction, the broker falls back to the original data until the next successful compaction, so readCompacted consumers may briefly see older values for a key.

## Checked

2026-11-03. Confirmed against the pulsar-site pages cookbooks-compaction and concepts-topic-compaction: the two-pass algorithm and tombstones, compaction horizon, null-key setting, threshold and compact commands, `readCompacted(true)` and the missing-ledger fallback. Removed the invented Verify step.

Method: documentation only; no commands were run.
