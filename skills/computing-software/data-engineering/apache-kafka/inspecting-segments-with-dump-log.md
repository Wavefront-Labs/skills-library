---
id: computing-software.data-engineering.apache-kafka.inspecting-segments-with-dump-log
name: inspecting-segments-with-dump-log
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-dump-log, log-segments, troubleshooting, transactions, kafka-operations]
level: advanced
status: docs-checked
description: "Inspect Kafka log segments, indexes and transaction markers with kafka-dump-log.sh to debug corruption, timestamps, compaction, producer ids and __consumer_offsets."
sources:
  - https://kafka.apache.org/documentation/#log
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/DumpLogSegments.java
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/TransactionsCommand.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting segments with kafka-dump-log.sh

Partition directories (`<log.dir>/<topic>-<partition>/`) contain `<baseOffset>.log` (records), `.index` (offset index), `.timeindex`, `.snapshot` (producer state), `leader-epoch-checkpoint`. `kafka-dump-log.sh` (class `DumpLogSegments`) decodes them offline on the broker host.

```bash
D=/data1/kafka/orders-3
kafka-dump-log.sh --files $D/00000000000001234567.log | head
# batch-level: offsets, producerId, producerEpoch, partitionLeaderEpoch, isTransactional, isControl, timestamp type and max timestamp, size, magic, compresscodec, crc
kafka-dump-log.sh --files $D/00000000000001234567.log --print-data-log --max-bytes 1000000 | head -50
# adds per-record offset, key, payload (as string), headers
kafka-dump-log.sh --files $D/00000000000001234567.index,$D/00000000000001234567.timeindex --index-sanity-check
kafka-dump-log.sh --files $D/00000000000001234567.log --deep-iteration   # deep instead of shallow iteration (set automatically by --print-data-log)
```

## Common investigations
- **Timestamps** (retention not deleting): check `CreateTime` of batches; a far-future timestamp in a segment keeps it from expiring. The `.timeindex` dump shows max timestamp per index entry.
- **Transactions**: control batches (`isControl: true`) with `endTxnMarker: COMMIT/ABORT` and `producerId`. A transactional batch with no marker later in the log points to a hanging transaction (confirm with `kafka-transactions.sh find-hanging`).
- **Compaction**: dump before/after to see which keys survive; with `--print-data-log` a record prints its key and, when it has a value, `payload:`, so a tombstone shows a key and no payload.
- **Corruption**: `--verify-index-only` checks an index without printing it and `--index-sanity-check` checks index sanity; dump the data file to see where parsing fails. Decide on repair only after confirming other replicas hold good copies.
- **Consumer offsets**: `--offsets-decoder` parses `__consumer_offsets` log data (the topic has `offsets.topic.num.partitions` partitions, default 50).
- **Transaction state**: `--transaction-log-decoder` parses `__transaction_state`.
- **KRaft metadata**: `--cluster-metadata-decoder --files <metadata.log.dir>/__cluster_metadata-0/...log` parses cluster metadata records (topic creations, configs, registrations); the KRaft docs also show `--cluster-metadata-decoder` on a checkpoint file. `kafka-metadata-shell.sh` inspects the metadata partition interactively.
- Other decoders: `--remote-log-metadata-decoder` and `--share-group-state-decoder`; `--key-decoder-class` and `--value-decoder-class` take custom decoders; `--max-message-size` sets the largest message size.

## Safety
The tool only reads, but the active segment of a live partition may end in a partially written tail (the tool reports trailing bytes); prefer closed segments, or copy files elsewhere if unsure.

## Verify
- [ ] The question (bad timestamp, missing marker, surviving key) is answered with a specific offset and batch.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed against DumpLogSegments.java: `--files`, `--print-data-log`, `--max-bytes`, `--max-message-size`, `--deep-iteration` (automatic with `--print-data-log`), `--index-sanity-check`, `--verify-index-only`, `--offsets-decoder`, `--transaction-log-decoder`, `--cluster-metadata-decoder`, `--remote-log-metadata-decoder`, `--share-group-state-decoder`, the key and value decoder class options, the batch fields printed, control-batch `endTxnMarker` output and the key/payload printing rule; `kafka-transactions.sh find-hanging` (TransactionsCommand source); `offsets.topic.num.partitions` default 50 (GroupCoordinatorConfig). Removed: the `payload: null` tombstone claim (value-less records print no payload), the group-to-partition hash formula, the CorruptRecordException and delete-the-partition-directory advice, the 3.3 version gate, and the compressed-batch wording.

Method: documentation only; no commands were run.
