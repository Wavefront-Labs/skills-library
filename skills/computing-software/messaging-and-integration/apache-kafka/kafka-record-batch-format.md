---
id: computing-software.messaging-and-integration.apache-kafka.kafka-record-batch-format
name: kafka-record-batch-format
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, record-batch, magic-2, crc-32c, control-batch]
level: sme
status: docs-checked
description: "Decode the on-disk RecordBatch (magic 2): header fields, attribute bits, CRC-32C coverage, compaction effects and control batches."
sources:
  - https://kafka.apache.org/42/implementation/message-format/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read Kafka's record batch layout accurately. Messages are always written in batches; a batch holds one or more records.

Batch header fields in order: baseOffset int64, batchLength int32, partitionLeaderEpoch int32, magic int8 (current value 2), crc uint32, attributes int16, lastOffsetDelta int32, baseTimestamp int64, maxTimestamp int64, producerId int64, producerEpoch int16, baseSequence int32, recordsCount int32, then the records. With compression, the compressed record data follows the record count directly.

Attributes: bits 0-2 compression (0 none, 1 gzip, 2 snappy, 3 lz4, 4 zstd); bit 3 timestampType; bit 4 isTransactional; bit 5 isControlBatch; bit 6 hasDeleteHorizonMs; bits 7-15 unused.

Sizing: total batch size on disk is batchLength + 12 bytes (8-byte baseOffset plus 4-byte batchLength).

CRC: CRC-32C (Castagnoli) over attributes to the end of the batch. partitionLeaderEpoch is excluded so the CRC need not be recomputed when the broker assigns it.

Compaction keeps the first and last offset and sequence numbers of the original batch, so producer state can be restored after reload; a batch can become empty after cleaning yet be kept to preserve the producer's last sequence number. baseTimestamp is not preserved and may change, and may be set to a deletion time (with the delete-horizon bit) for null-payload records or transaction markers.

Control batches hold one control record (key: version int16, type int16 where 0 is abort and 1 is commit). Clients must not pass them to applications.

Records use varints (as in Protobuf): length, attributes, timestampDelta, offsetDelta, key, value, headers. Header keys are non-null; values may be null; order is preserved.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 message-format page. Corrected the compaction paragraph (transaction markers, not aborted markers; dropped the OutOfSequence claim). Other claims unchanged. No hands-on run.
