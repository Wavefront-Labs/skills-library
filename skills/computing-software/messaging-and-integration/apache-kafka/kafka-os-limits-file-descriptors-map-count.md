---
id: computing-software.messaging-and-integration.apache-kafka.kafka-os-limits-file-descriptors-map-count
name: kafka-os-limits-file-descriptors-map-count
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, file-descriptors, vm-max-map-count, os-tuning, socket-buffer]
level: practitioner
status: docs-checked
description: "Size OS limits for a broker: file descriptors (100000 to start), vm.max_map_count and socket buffers."
sources:
  - https://kafka.apache.org/42/operations/hardware-and-os/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid OS-limit crashes on brokers with many partitions.

File descriptors: Kafka uses them for log segments and connections. Segments need roughly (number_of_partitions)*(partition_size/segment_size) descriptors, plus connections. The docs suggest starting at 100000 allowed descriptors for broker processes. mmap() keeps a file reference even after close(), released only when no mappings remain.

vm.max_map_count: each log segment has an index file and a timeindex file, each using one memory map area, so every partition needs at least 2. A default near 65535 can be exceeded at about 50000 partitions per broker, crashing it with OutOfMemoryError (Map failed). Segments per partition usually exceed one, so the real limit is lower.

Max socket buffer size: can be raised for high-performance transfers between data centers; the page links to external tuning guidance. It gives no commands for setting any of these limits.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 hardware-and-os page. Removed the claims about the write_throughput*30 memory estimate, socket.send/receive.buffer.bytes names and Solaris testing (not confirmed in my read; the page only cautions about Windows). No hands-on run.
