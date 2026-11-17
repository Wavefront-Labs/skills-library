---
id: computing-software.messaging-and-integration.debezium.postgresql-decimal-money-and-binary-handling
name: postgresql-decimal-money-and-binary-handling
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, data-types, decimal, money]
level: practitioner
status: docs-checked
description: "Tune decimal.handling.mode, money.fraction.digits, binary.handling.mode and hstore.handling.mode for PostgreSQL events."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Several connector properties decide how PostgreSQL types appear in events.

`decimal.handling.mode` (default `precise`) covers DECIMAL and NUMERIC:

- `precise`: `java.math.BigDecimal`, binary form in events.
- `double`: double values; easier but can lose precision.
- `string`: formatted strings, easy to read but the real type is lost.

`money.fraction.digits` (default `2`) sets the scale when the `money` type is converted to `BigDecimal`; it applies only with `precise`.

`binary.handling.mode` (default `bytes`) controls `bytea`: `bytes`, `base64`, `base64-url-safe` or `hex`.

`hstore.handling.mode` (default `json`) renders hstore as a JSON string such as `{"key" : "val"}`, or as a Connect `MAP` when set to `map`.

`include.unknown.datatypes` (default `false`): unknown types are omitted with a warning. Setting `true` emits an opaque binary value, but consumers risk compatibility breaks if Debezium later supports the type as a logical type.

```json
"decimal.handling.mode": "string",
"binary.handling.mode": "base64"
```

Gotcha: `precise` represents values in binary form in change events, while `string` is easy to consume but loses the real type.

Check: insert a NUMERIC(10,2) value and read the event through your actual converter.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: decimal.handling.mode, money.fraction.digits, binary.handling.mode, hstore.handling.mode, include.unknown.datatypes.
Removed or reworded: the base64-in-JSON claim.
Method: documentation only; no commands were run.
