---
id: computing-software.messaging-and-integration.debezium.postgresql-toasted-values-placeholder
name: postgresql-toasted-values-placeholder
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, toast, unavailable-value-placeholder, replica-identity]
level: advanced
status: docs-checked
description: "Understand why unchanged TOAST columns are missing from PostgreSQL events and how unavailable.value.placeholder marks them."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PostgreSQL stores values larger than roughly 8 KB with TOAST. When a row is updated and a TOASTed column is unchanged, logical decoding omits that value unless the column is part of the replica identity. Debezium cannot safely read it out of band because that would create race conditions, so it follows fixed rules:

- Tables with `REPLICA IDENTITY FULL`: TOAST values appear in `before` and `after` like any other column.
- Tables with `REPLICA IDENTITY DEFAULT`: an unchanged TOAST column is absent from an `UPDATE`, and a `DELETE` has no TOAST columns in `before`. The connector emits a placeholder instead.

The placeholder is set by `unavailable.value.placeholder`, default `__debezium_unavailable_value`. If the value starts with `hex:`, the rest must be an even number of hex characters or configuration validation fails.

```json
"unavailable.value.placeholder": "__debezium_unavailable_value"
```

Consumers and sinks must treat that string as "unchanged", not as data.

Options: set `ALTER TABLE ... REPLICA IDENTITY FULL` for tables with big text or JSON columns, or handle the placeholder in consumers.

Related: `schema.refresh.mode=columns_diff_exclude_unchanged_toast` reduces schema refreshes on tables with rarely updated TOAST columns.

Check: update a small column on a row with a large text column and inspect the `after` payload.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: TOAST behaviour and race-condition rationale, rules for FULL and DEFAULT, unavailable.value.placeholder default and hex: prefix, schema.refresh.mode option.
Removed or reworded: the naive-upsert claim and the downstream-filter fix.
Method: documentation only; no commands were run.
