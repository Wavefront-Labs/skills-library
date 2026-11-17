---
id: computing-software.messaging-and-integration.debezium.mysql-tinyint-boolean-converter
name: mysql-tinyint-boolean-converter
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, custom-converter, boolean, tinyint]
level: practitioner
status: docs-checked
description: "Apply TinyIntOneToBooleanConverter so TINYINT(1) columns map consistently between snapshot and streaming."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
During a snapshot the JDBC driver reports `BOOLEAN` columns as `TINYINT(1)`, and Debezium builds the snapshot schema from that. After the switch to streaming, the schema can differ, leaving inconsistent mappings for boolean columns. The `TinyIntOneToBooleanConverter` makes them uniform.

```
converters=tinyint-one-to-boolean
tinyint-one-to-boolean.type=io.debezium.connector.binlog.converters.TinyIntOneToBooleanConverter
tinyint-one-to-boolean.selector=.*.MY_TABLE.DATA
tinyint-one-to-boolean.length.checker=false
```

Both extra properties are optional:

- `selector`: a regular expression for the tables or columns to convert. If omitted, every TINYINT column maps to a logical boolean.
- `length.checker`: by default the converter confirms the type has length 1. Set `false` to skip that check.

If you do not configure a selector and want the length check kept, omit `length.checker` or leave it `true`.

Check: compare a snapshot event and a streamed event for the same column; both should show the same Connect type.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: snapshot versus streaming mapping of BOOLEAN and TINYINT(1), the converter class and example, selector and length.checker semantics.
Removed or reworded: the Avro-compatibility gotcha, the comma-separated converters note.
Method: documentation only; no commands were run.
