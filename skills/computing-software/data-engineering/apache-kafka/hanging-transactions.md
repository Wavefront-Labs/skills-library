---
id: computing-software.data-engineering.apache-kafka.hanging-transactions
name: hanging-transactions
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-transactions, hanging-transactions, last-stable-offset, kafka-transactions-tool, read-committed, transaction-timeout, stuck-consumers]
level: advanced
status: docs-checked
description: "Find and abort hanging Kafka transactions that pin the last stable offset and stall read_committed consumers, using kafka-transactions.sh find-hanging and abort."
sources:
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-664%3A+Provide+tooling+to+detect+and+abort+hanging+transactions
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://kafka.apache.org/40/configuration/broker-configs/
  - https://kafka.apache.org/39/getting-started/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hanging transactions

**Goal:** recover when `read_committed` consumers stop making progress on a partition even though data is arriving.

## Symptom
- Consumer lag grows on one or a few partitions; consumers poll but get nothing.
- `LogEndOffset` keeps rising while the **last stable offset (LSO)** stays fixed. `read_committed` consumers can only read up to the LSO, the first offset of the oldest open transaction.

Normally the coordinator aborts transactions after `transaction.timeout.ms` (producer setting, default 60000 ms; the broker rejects a larger request via `transaction.max.timeout.ms`, default 900000 ms = 15 minutes). A transaction **hangs** when it stays open past that bound because the coordinator lost track of it. Transaction partition verification (KIP-890, Kafka 3.6+) was added to prevent hanging transactions.

## Detect (Kafka 3.0+ tooling)
```bash
kafka-transactions.sh --bootstrap-server $BS list
kafka-transactions.sh --bootstrap-server $BS describe --transactional-id payments-tx-0
kafka-transactions.sh --bootstrap-server $BS describe-producers --topic payments --partition 3
kafka-transactions.sh --bootstrap-server $BS find-hanging --broker-id 2
kafka-transactions.sh --bootstrap-server $BS find-hanging --topic payments --partition 3
```
`describe-producers` shows `CurrentTransactionStartOffset` for each producer id; an old start offset on a busy partition is the culprit. `find-hanging` needs `--broker-id` or `--topic` to limit the search (`--partition` requires `--topic`) and lists transactions open longer than `--max-transaction-timeout`, in minutes (default 15).

## Abort
```bash
kafka-transactions.sh --bootstrap-server $BS abort --topic payments --partition 3 --start-offset 918273
# brokers older than 3.0 need all three of these instead of --start-offset:
kafka-transactions.sh --bootstrap-server $BS abort --topic payments --partition 3 \
  --producer-id 41027 --producer-epoch 12 --coordinator-epoch 7
```
The command needs administrative privileges. Once aborted, the LSO advances and consumers resume.

## Prevention
- Upgrade brokers to 3.6+ (transaction verification, KIP-890) and clients to recent versions.
- Keep `transaction.timeout.ms` small for stream processors; a long transaction delays all `read_committed` readers.
- Alert on `find-hanging` output from a scheduled job. KIP-664 also proposes a `PartitionsWithLateTransactionsCount` gauge (ReplicaManager group): check your broker version's monitoring page before relying on it.

## Verify
- [ ] After abort, `describe-producers` shows no old open transaction and consumer lag drains.
- [ ] A periodic `find-hanging` check returns empty.

## Checked
2026-10-28. Confirmed in TransactionsCommand source (Kafka 3.9), KIP-664, the 3.9 upgrade notes and the Kafka config pages: subcommands and flags (`list`, `describe`, `describe-producers`, `find-hanging --broker-id/--topic/--partition/--max-transaction-timeout` with default 15 minutes, `abort --start-offset` and the pre-3.0 `--producer-id/--producer-epoch/--coordinator-epoch`), `CurrentTransactionStartOffset`, `transaction.timeout.ms` default 60000, `transaction.max.timeout.ms` default 900000, KIP-890 verification added in 3.6. Corrected: `find-hanging` threshold is `--max-transaction-timeout` in minutes and needs `--broker-id` or `--topic`; the producer-id/epoch form of `abort` is for brokers older than 3.0. Removed: KAFKA-12671, ACL specifics, the claim about compaction, and the `kafka.log` metric remark.
Method: documentation only; no commands were run.
