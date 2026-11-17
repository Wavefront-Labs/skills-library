---
id: computing-software.cloud-infrastructure-engineering.vector.log-event-data-model
name: log-event-data-model
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [log-events, data-model, schema-neutral, timestamps, types, vrl, vector]
level: intro
status: docs-checked
description: "Understand what a Vector log event is, its field types and how timestamps are coerced."
sources:
  - https://vector.dev/docs/architecture/data-model/log/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Vector log event is a structured representation of a point-in-time event: an arbitrary set of key/value fields, nested as deeply as needed. Example as JSON:

```json
{"log": {"custom": "field", "host": "my.host.com", "message": "Hello world", "timestamp": "2020-11-01T21:15:47+00:00"}}
```

Vector is schema neutral. It requires no specific fields, so it can handle legacy and future schemas; each component documents the fields it adds.

Field types:

- Strings are UTF-8 and bounded only by memory.
- Integers are signed, up to 64 bits.
- Floats are 64-bit IEEE 754.
- Booleans, null values (for JSON compatibility), maps (string keys to any value) and arrays (sequences of any value).
- Timestamps are stored as UTC.

Timestamp handling: when a format has no formal timestamp type, such as JSON, Vector ingests the timestamp in its primitive form (string or integer). Coerce it with a remap transform and the `parse_timestamp` VRL function. If a received timestamp has no timezone information, Vector assumes local time and converts it to UTC.

Practical consequence: do not assume a field exists. Guard access in VRL and set `timestamp` explicitly when a source does not provide one.

Verify by sending a sample event through the `console` sink with `encoding.codec: json` and reading the field types in the output.

## Checked

2026-11-03. Read architecture/data-model/log and sinks/console. Confirmed: schema neutrality, UTF-8 strings, signed 64-bit integers, 64-bit IEEE 754 floats, null for JSON compatibility, UTC timestamps, `parse_timestamp` coercion, local-time assumption for zone-less timestamps, and the console sink `codec: json` encoding. Nothing removed.

Method: documentation only; no commands were run.
