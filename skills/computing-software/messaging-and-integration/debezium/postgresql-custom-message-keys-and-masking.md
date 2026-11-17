---
id: computing-software.messaging-and-integration.debezium.postgresql-custom-message-keys-and-masking
name: postgresql-custom-message-keys-and-masking
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, message-key, column-mask, filtering]
level: practitioner
status: docs-checked
description: "Use message.key.columns, column.exclude.list and column.mask.with.length.chars to shape keys and hide sensitive columns."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the message key is the table primary key. For tables without a primary key, or when you need a different partition key, set `message.key.columns`. Each entry is `<fully-qualified_tableName>:<keyColumn>,<keyColumn>` and the table part is a regular expression of the form `<schemaName>.<tableName>`. Separate multiple tables with semicolons.

```json
"message.key.columns": "public.orders:customer_id,order_id"
```

Column filtering uses anchored regular expressions on fully-qualified names `schemaName.tableName.columnName`; the whole name must match, not a substring:

- `column.exclude.list`: columns left out of change event values.
- `column.include.list`: the inverse; choose one of include or exclude.
- `column.mask.with.length.chars`: replaces character column values with that many asterisks. The property name carries the length, for example `column.mask.with.12.chars`. A length of `0` produces an empty string.

```json
"column.exclude.list": "public.users.password_hash",
"column.mask.with.12.chars": "public.users.ssn"
```

Check: consume one event for the table and confirm excluded fields are absent and masked fields show asterisks.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: message.key.columns format and semicolons, anchored regular expressions, column.exclude.list and include.list, column.mask.with.length.chars including 0.
Removed or reworded: two gotchas about excluded key columns and masked source data.
Method: documentation only; no commands were run.
