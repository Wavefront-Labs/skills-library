---
id: computing-software.messaging-and-integration.debezium.postgresql-replica-identity-and-before-values
name: postgresql-replica-identity-and-before-values
category: computing-software
field: messaging-and-integration
product: debezium
tags: [postgresql, replica-identity, update, delete]
level: practitioner
status: docs-checked
description: "Choose REPLICA IDENTITY DEFAULT, NOTHING, FULL or INDEX to control the before values in PostgreSQL update and delete events."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`REPLICA IDENTITY` is a table-level PostgreSQL setting that decides how much of the previous row logical decoding supplies on `UPDATE` and `DELETE`. It directly shapes the `before` field in Debezium events.

- `DEFAULT`: events carry previous values for primary key columns only. On `UPDATE`, only changed key columns appear. A table with no primary key emits only create events, with no updates or deletes.
- `NOTHING`: no previous values at all.
- `FULL`: previous values of all columns.
- `INDEX index-name`: previous values of the columns in that index; updates also carry the new indexed values.

Set it with standard DDL:

```sql
ALTER TABLE public.orders REPLICA IDENTITY FULL;
```

Choose `FULL` when consumers need the whole old row, or when the table has TOAST columns that must always appear in events (see postgresql-toasted-values-placeholder).

Gotcha: for a table without a primary key, the connector will not publish updates or deletes under `DEFAULT`. Either add a key, use `REPLICA IDENTITY FULL`, or point to a unique index with `INDEX`.

Custom message keys can supplement keys for tables lacking a primary key via `message.key.columns`.

Check: update a row in a test table and confirm the `before` field holds the columns you expect.

## Checked

2026-11-03. Page used: the Debezium postgresql connector reference, https://debezium.io/documentation/reference/stable/connectors/postgresql.html.
Confirmed against it: DEFAULT, NOTHING, FULL and INDEX behaviour, tables without a primary key emitting only create events, message.key.columns.
Removed or reworded: the WAL-volume claim.
Method: documentation only; no commands were run.
