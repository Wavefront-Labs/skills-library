---
id: computing-software.messaging-and-integration.debezium.outbox-event-router-payload-and-additional-fields
name: outbox-event-router-payload-and-additional-fields
category: computing-software
field: messaging-and-integration
product: debezium
tags: [outbox, smt, payload, json-expansion]
level: advanced
status: docs-checked
description: "Expand JSON payloads, carry Avro bytes and place extra outbox columns in headers, envelope or partition."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Payload handling in the outbox router:

JSON string payloads normally arrive escaped. To emit real JSON, set:

```
transforms.outbox.table.expand.json.payload=true
value.converter=org.apache.kafka.connect.json.JsonConverter
```

If content is missing or cannot be parsed, it is kept as is. Related options: `table.json.payload.null.behavior` (default `ignore`, or `optional_bytes`) and `table.json.payload.empty.array.behavior` (default `ignore`, or `optional_string`).

Avro payloads: use a binary column type such as `bytea` and the pass-through converter:

```
value.converter=io.debezium.converters.BinaryDataConverter
value.converter.delegate.converter.type=org.apache.kafka.connect.json.JsonConverter
value.converter.delegate.converter.type.schemas.enable=false
```

`BinaryDataConverter` cannot serialise heartbeat, transaction metadata or schema change events, so name a delegate converter for those; with a registry the delegate can be an Apicurio or Confluent `AvroConverter` (third-party libraries needed).

Extra columns: `table.fields.additional.placement` is a comma-separated list of `column:placement[:alias]`.

```
transforms.outbox.table.fields.additional.placement=eventType:header:type
```

Placements are `header`, `envelope` and `partition`. A `partition` placement controls the target partition and ignores aliases. `table.field.additional.missing` (default `error`, or `ignore`) decides what happens when a listed column is absent.

Gotcha: with extra envelope fields the message value becomes an envelope, not just the payload.

Check: consume one message and confirm headers include the event id.

## Checked

2026-11-08. Confirmed against the Debezium page transformations/outbox-event-router, read in full: table.expand.json.payload with JsonConverter, null and empty array behaviours, BinaryDataConverter and delegate converters, third-party library note, the column:placement:alias syntax, header, envelope and partition placements and table.field.additional.missing. Nothing removed.

Method: documentation only; no commands were run.
