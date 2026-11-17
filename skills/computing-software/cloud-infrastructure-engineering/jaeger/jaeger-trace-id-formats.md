---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-trace-id-formats
name: jaeger-trace-id-formats
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, trace-id, base64-trace-id, 128-bit-ids, kafka-json-encoding]
level: advanced
status: docs-checked
description: "Explain why trace IDs look different in Kafka and the UI: 16 bytes as hex, uint64 pairs or base64 in Protobuf JSON."
sources:
  - https://www.jaegertracing.io/docs/2.22/faq/
  - https://www.jaegertracing.io/docs/2.22/deployment/frontend-ui/
  - https://www.jaegertracing.io/docs/2.22/operations/performance-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: convert trace IDs between systems.

At the data model level a Jaeger trace ID is a sequence of 16 bytes, represented several ways:
- UI: hex-encoded strings, 32 characters for 128-bit IDs (more common in OpenTelemetry), or 16 characters for legacy 64-bit IDs. Example: `7e90c0eca22784ec7e90c0eca22784ec`.
- Backend domain model: a pair of unsigned 64-bit integers, big-endian, for efficiency because a Go byte slice requires an extra memory allocation.
- Original Thrift model: also a pair of unsigned 64-bit integers.
- Protobuf: a byte sequence, transmitted as is in binary.
- Protobuf JSON encoding: bytes serialized as base64. If the collector-Kafka-ingester pipeline uses JSON encoding, trace IDs look like `fpDA7KInhOx+kMDsoieE7A==`.

Convert base64 back to hex IDs recognized by the UI with a converter such as base64.guru's base64-to-hex tool.

Related UI setting: `traceIdDisplayLength` (default 7) controls how many characters of the ID are shown, and the link template function `pad_start` can pad IDs, for example `#{traceID | pad_start 32 0}`.

Kafka sharding uses trace IDs, so all spans of a trace go to the same partition.

## Checked

2026-11-03. Confirmed against the FAQ page: 16-byte IDs, hex in the UI (32 or 16 characters), pair of big-endian uint64 in the backend and Thrift, Protobuf bytes and base64 in JSON, and the example value. traceIdDisplayLength and pad_start are from the Frontend/UI page, and trace-ID partitioning of Kafka from the Performance Tuning page. Nothing removed.
Method: documentation only; no commands were run.
