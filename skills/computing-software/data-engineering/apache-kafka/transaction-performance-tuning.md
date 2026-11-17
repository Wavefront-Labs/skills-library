---
id: computing-software.data-engineering.apache-kafka.transaction-performance-tuning
name: transaction-performance-tuning
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, transaction-batching, transactions, exactly-once, commit-interval-ms, transaction-timeout, kafka-delivery-semantics]
level: advanced
status: docs-checked
description: "Make Kafka transactions fast: batch many records per transaction, size commit intervals, set transaction.timeout.ms, and understand the read_committed latency cost."
sources:
  - https://www.confluent.io/blog/transactions-apache-kafka/
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/configuration/kafka-streams-configs/
  - https://kafka.apache.org/39/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction performance tuning

## Cost model
Each transaction adds fixed overhead regardless of size: `AddPartitionsToTxn` and `AddOffsetsToTxn` RPCs to the transaction coordinator, a commit request, and **commit markers** written to every partition touched (plus the `__transaction_state` log write). So overhead is per transaction, not per record:
- 1 record per transaction: throughput collapses (each send is a multi-RPC round trip).
- Many records per transaction: the fixed overhead is amortised.

## Tune
- **Batch by time or count**: commit every N ms or every M records, not per input record. Kafka Streams with `processing.guarantee=exactly_once_v2` does this via `commit.interval.ms` (default 100 ms under EOS, 30 s otherwise).
- Keep normal producer batching on (`linger.ms`, `batch.size`, compression): transactions do not disable it.
- `transaction.timeout.ms` (default 60000 ms; the broker rejects larger requests via `transaction.max.timeout.ms`, default 900000 ms): must exceed the longest time a transaction stays open, including processing hiccups; otherwise the coordinator proactively aborts it and the producer's next transactional call fails. Do not set it huge: a stuck open transaction blocks read_committed consumers until it times out.
- Fewer partitions touched per transaction = fewer markers. Writing to very many partitions per transaction is slow; group outputs or reduce fan-out.
- Use EOS v2 (`exactly_once_v2`, requires brokers 2.5 or newer) in Streams: one producer per thread instead of per task (KIP-447).

## Consumer side latency
`isolation.level=read_committed` consumers only see records up to the **last stable offset**. End-to-end latency is therefore at least the commit interval. A 1 s commit interval means ~1 s added latency for downstream readers. Choose the interval as the latency/throughput trade-off.

## Monitoring
- Producer (`producer-metrics`): `txn-begin-time-ns-total`, `txn-send-offsets-time-ns-total`, `txn-commit-time-ns-total`, `txn-abort-time-ns-total`, `record-queue-time-avg`.
- Consumer: lag under `read_committed`.
- Hanging transactions: `kafka-transactions.sh find-hanging`.

## Verify
- [ ] Perf test with your real fan-out at two commit intervals; pick the one that meets both throughput and latency SLOs.
- [ ] No producer fencing errors under peak processing pauses (timeout headroom).

## Checked
2026-10-28. Confirmed in the Kafka 3.9/4.0 Streams config pages, producer and broker config tables, the 3.9 monitoring page, KIP-447, KIP-664 and the Confluent transactions blog: `commit.interval.ms` default 30000 and 100 ms under exactly-once, `exactly_once_v2` needs brokers 2.5+, producer transaction metrics, `transaction.timeout.ms` 60000 and `transaction.max.timeout.ms` 900000, per-thread producers under EOS v2, AddPartitionsToTxn/commit marker cost model. Removed: the percent overhead figure, the 100 ms-1 s and 500-partition figures, the exception names after timeout, and unverified broker metric names.
Method: documentation only; no commands were run.
