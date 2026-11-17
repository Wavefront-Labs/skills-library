---
id: computing-software.messaging-and-integration.redpanda.transactions-semantics-and-tuning
name: transactions-semantics-and-tuning
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [transactions, exactly-once, transactional-id, producer-ids, max-concurrent-producer-ids, read-committed]
level: advanced
status: docs-checked
description: "Use Redpanda transactions: transactional.id, atomicity versus exactly-once, producer ID and coordinator limits, timeouts, internal tx topic growth, and compaction interactions."
sources:
  - https://docs.redpanda.com/streaming/current/develop/transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Transactions are Kafka-compatible and enabled by default (`enable_transactions` is true). Clients must use the Transactions API for atomic publishing of multiple messages and for exactly-once stream processing. Set `transactional.id` in the producer config; it identifies the producer across sessions. Exactly-once semantics need transactions plus idempotent producers (the page's Java example sets `acks=all`, idempotence true and a `TRANSACTIONAL_ID_CONFIG`, then calls `initTransactions`, `beginTransaction`, `commitTransaction`). Atomicity is not guaranteed when remote recovery is used.

If a transaction fails before `commitTransaction` completes, assume it did not execute. If it fails after the commit attempt, the true status is unknown and the application must discover it.

**Producer ID limits.** For heavy production use, set `max_concurrent_producer_ids` and `transactional_id_expiration_ms` to avoid OOM crashes. With `kafka_connections_max` set, the lower bound is `kafka_connections_max` / number of shards and the upper bound is `topic_partitions_per_shard` * `kafka_connections_max`; otherwise start at 1000-5000 per shard. Set expiration to the longest expected transaction plus a buffer (for example 2-4 hours for 30-minute transactions). Reuse producers and avoid random transactional IDs. Watch `vectorized_cluster_producer_state_manager_evicted_producers`, which should be 0 in steady state; above 0 the shard is exceeding the limit.

**Timeouts and limits.** A very large `transaction.timeout.ms` can block `read_committed` consumers. Cluster capacity is `max_transactions_per_coordinator * transaction_coordinator_partitions` (default 50 partitions); beyond it old sessions are terminated. Transaction metadata lives in `kafka_internal/tx`; manage its disk use with `transaction_coordinator_delete_retention_ms` and `transactional_id_expiration_ms`. Keep delete retention at or above expiration. Use maintenance mode during rolling upgrades.

**Compaction.** Aborted data is removed; `log_compaction_tx_batch_removal_enabled` also removes commit and abort markers using `delete.retention.ms`; this is not applied when Tiered Storage is enabled.

## Checked

2026-11-04. Defaults, limits formulas, metrics, internal topic and compaction settings were confirmed on the Transactions page. The condition line about delete retention was read as a recommendation.

Method: documentation only; no commands were run.
