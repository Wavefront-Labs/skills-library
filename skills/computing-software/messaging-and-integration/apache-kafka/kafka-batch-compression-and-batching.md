---
id: computing-software.messaging-and-integration.apache-kafka.kafka-batch-compression-and-batching
name: kafka-batch-compression-and-batching
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, compression, batching, gzip-snappy-lz4-zstd]
level: practitioner
status: docs-checked
description: "Use producer batching and end-to-end batch compression (GZIP, Snappy, LZ4, ZStandard) to trade latency for throughput."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: raise throughput and reduce network use through batching and compression.

Batching: the producer accumulates records in memory and sends larger batches in one request. Batching can be bounded by a size and a wait time (the docs give an example of 64kB or 10 ms), trading a little latency for fewer, larger I/O operations on the servers.

Compression: compressing messages one at a time gives poor ratios because the redundancy lies between messages (JSON field names, user agents, common values). Kafka compresses a whole batch instead. Supported codecs: GZIP, Snappy, LZ4 and ZStandard.

Path of a compressed batch:
- The broker decompresses it only to validate it (for example, that the record count matches the batch header).
- It is written to disk compressed and stays compressed in the log.
- It is sent to consumers compressed; the consumer decompresses it.

This matters most when the bottleneck is network bandwidth, such as pipelines between data centers over a WAN.

Producers send directly to the partition leader with no routing tier; any node can answer metadata requests about live servers and partition leaders.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Efficiency, Producer, Consumer, Delivery Semantics, Static Membership and Using Transactions sections read in full)
