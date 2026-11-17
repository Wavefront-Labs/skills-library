---
id: computing-software.messaging-and-integration.apache-kafka.kafka-log-cleaner-tuning
name: kafka-log-cleaner-tuning
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, log-cleaner, log-cleanup-policy, uncleanable-partitions-count, max-compaction-delay-secs]
level: advanced
status: docs-checked
description: "Operate the log cleaner threads: how compaction picks logs, memory per key, enabling it, and which metrics to watch."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run log compaction predictably.

How a cleaner thread works:
1. Choose the log with the highest ratio of head to tail.
2. Build a summary of the last offset for each key in the head.
3. Recopy the log, dropping keys that appear later. New segments are swapped in immediately, so only one extra segment of disk is needed.

The summary is a compact hash table using exactly 24 bytes per entry. With 8GB of cleaner buffer, one iteration can clean about 366GB of log head, assuming 1kB messages.

Configuration:
- The log cleaner is enabled by default and starts the cleaner thread pool.
- Compaction is selected with `log.cleanup.policy=compact`, a broker setting in server.properties that affects every topic without a configuration override.
- `log.cleaner.min.compaction.lag.ms`: if unset, every segment except the active one is eligible.
- `log.cleaner.max.compaction.lag.ms`: bounds how long a low-traffic log can stay ineligible. If unset, logs that do not exceed `min.cleanable.dirty.ratio` are not compacted. This deadline is not a hard guarantee; it still depends on cleaner thread availability.

Monitor the metrics `uncleanable-partitions-count`, `max-clean-time-secs` and `max-compaction-delay-secs`.

Cleaning does not block reads and can be throttled to a configured I/O rate.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Design page (Log Compaction). Removed: per-topic 'cleanup.policy' key, which the page does not show.

Method: documentation only; no commands were run.
