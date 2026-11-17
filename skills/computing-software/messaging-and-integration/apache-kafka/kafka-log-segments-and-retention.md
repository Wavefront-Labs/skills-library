---
id: computing-software.messaging-and-integration.apache-kafka.kafka-log-segments-and-retention
name: kafka-log-segments-and-retention
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, log-segments, retention-ms, retention-bytes, segment-files]
level: practitioner
status: docs-checked
description: "Know how partition logs are laid out as segment files and how time and size retention delete whole segments."
sources:
  - https://kafka.apache.org/42/implementation/log/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the on-disk log so retention behaves as expected.

A topic named my-topic with two partitions has directories my-topic-0 and my-topic-1 holding data files. Each message is identified by a 64-bit offset. Each segment file is named by the offset of its first message, so the first is 00000000000000000000.log, and later files are roughly the configured maximum segment size apart. Appends always go to the last file, which rolls over to a fresh file at a configurable size (the docs say, for example, 1GB).

Reads take a 64-bit offset and a maximum chunk size; the broker finds the segment with a binary search over an in-memory range and reads from the computed file offset. Fetching an offset that no longer exists raises OutOfRangeException, and the client can reset or fail.

Deletion is per whole segment, using two criteria:
- Time: the largest record timestamp in a segment defines when the whole segment expires.
- Size: disabled by default; when enabled, the oldest segments are deleted until the partition fits the limit.

If both are enabled, a segment eligible under either policy is deleted. Deletes use a copy-on-write segment list so binary searches can run on an immutable snapshot while deletes proceed.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 implementation/log page. Claims matched; reworded the copy-on-write sentence and dropped the unsupported "record order is irrelevant". The page gives no config key names. No hands-on run.
