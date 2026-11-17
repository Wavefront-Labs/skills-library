---
id: computing-software.data-engineering.apache-kafka.record-headers
name: record-headers
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, record-headers, message-metadata, tracing, content-type, kafka-producer]
level: practitioner
status: docs-checked
description: "Use Kafka record headers for metadata (trace ids, content type, schema version, source) without bloating payloads, and know which tools keep or drop them."
sources:
  - https://kafka.apache.org/documentation/#recordheader
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-82+-+Add+Record+Headers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Record headers

Headers are key (string) / value (bytes) pairs on each record, separate from key and value; the Java `Headers` API has `add` and `lastHeader`.

## Produce and read
```java
ProducerRecord<String, byte[]> r = new ProducerRecord<>("orders", key, payload);
r.headers().add("traceparent", traceparent.getBytes(UTF_8))
           .add("content-type", "application/avro".getBytes(UTF_8))
           .add("source", "checkout-svc".getBytes(UTF_8));
producer.send(r);
// consumer
Header h = record.headers().lastHeader("traceparent");
String tp = h == null ? null : new String(h.value(), UTF_8);
```

## Good uses
- Tracing context: W3C `traceparent`/`tracestate`.
- Routing/filtering metadata a consumer can check without deserialising the value (event type, tenant id).
- Content type / encoding, schema version for non-registry formats.
- Error context on dead-letter records (Kafka Connect sink: `errors.deadletterqueue.topic.name` plus optional `errors.deadletterqueue.context.headers.enable=true`).

## Rules
- Business data belongs in the value: headers are not part of the schema contract, not validated by Schema Registry, and easy to lose.
- Header values are raw bytes; agree on an encoding (UTF-8 strings) per key.
- Headers add to record size. Keep them short.
- Kafka Connect SMTs for headers: `InsertHeader` (static data), `DropHeaders` (by name), `HeaderFrom` (copy or move key/value fields into headers).
- Check each downstream tool to see whether it propagates headers.
- Do not put secrets or PII in headers; many tools log them.

## Verify
- [ ] Downstream processors propagate the headers you rely on (test each hop).

## Checked
2026-11-01. Confirmed against the Kafka 3.9 docs: `Headers` javadoc (`add`, `lastHeader`), Connect user guide (header SMTs `InsertHeader`, `DropHeaders`, `HeaderFrom`; `errors.deadletterqueue.*` settings). Removed: KIP/version claim, Python example, OpenTelemetry, MirrorMaker 2/Streams/Flink/Spark propagation claims, `__connect.errors.*` names, console-consumer property, compaction note.
Method: documentation only; no commands were run.
