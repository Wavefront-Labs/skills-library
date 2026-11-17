---
id: computing-software.messaging-and-integration.debezium.oracle-lob-capture-and-boolean-converter
name: oracle-lob-capture-and-boolean-converter
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, lob, custom-converter, boolean]
level: practitioner
status: docs-checked
description: "Enable lob.enabled for CLOB, NCLOB and BLOB capture and map Oracle NUMBER(1) to boolean with a converter."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
LOB capture is opt-in:

```json
"lob.enabled": "true"
```

With the default `false`, snapshot events include the current LOB values, but streamed events show the `unavailable.value.placeholder` constant for LOB columns. With `true`, the connector mines extra redo operation types for CLOB, NCLOB and BLOB writes, adding processing overhead. You cannot use the `hybrid` mining strategy together with `lob.enabled=true`.

Key behaviour: Oracle puts a LOB value in redo only when a DML statement explicitly sets or changes that LOB column. If an update does not touch it, the event carries the placeholder, not the current value. Consumers must treat the placeholder as unchanged.

Rollback caveat: `log.mining.include.internal.events` (default `false`) controls whether INTERNAL events are mined. They give the connector the row identifiers it needs to handle `ROLLBACK TO SAVEPOINT` for out-of-line LOBs. With `false`, a rolled-back statement may still produce events or stale LOB values.

Oracle versions before 23 simulate booleans with `NUMBER(1)`, which Debezium emits as `INT8`. To emit the logical boolean type instead:

```
converters=number-to-boolean
number-to-boolean.type=io.debezium.connector.oracle.converters.NumberOneToBooleanConverter
number-to-boolean.selector=.*.MY_TABLE.DATA
```

`selector` is an optional regular expression; omit it and every `NUMBER(1)` column converts.

## Checked

2026-11-08: read the Capturing large object data and INTERNAL events sections, the NUMBER(1) to Boolean converter section, and the lob.enabled, log.mining.include.internal.events and unavailable.value.placeholder property rows of the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc). Confirmed all behaviour, defaults and the converter configuration. Removed: the sink upsert gotcha and the test Check line, which the page does not state.

Method: documentation only; no commands were run.
