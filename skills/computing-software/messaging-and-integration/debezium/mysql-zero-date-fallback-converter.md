---
id: computing-software.messaging-and-integration.debezium.mysql-zero-date-fallback-converter
name: mysql-zero-date-fallback-converter
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, custom-converter, zero-date, temporal]
level: advanced
status: docs-checked
description: "Configure ZeroDateFallbackConverter to control what Debezium emits for MySQL 0000-00-00 DATE and DATETIME values."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MySQL and MariaDB allow `0000-00-00` and `0000-00-00 00:00:00`, which are not real instants. Debezium cannot represent them in its temporal types, so by default it collapses them to `null` (nullable column) or to the epoch (NOT NULL column). `ZeroDateFallbackConverter` lets you choose per type or per column.

```
converters=zero-date
zero-date.type=io.debezium.connector.binlog.converters.ZeroDateFallbackConverter
zero-date.target.types=DATE,DATETIME,TIMESTAMP
zero-date.fallback.date=NULL
zero-date.fallback.datetime=2000-01-01 00:00:00
zero-date.fallback.timestamp=1970-01-01T00:00:00Z
zero-date.column.appdb.users.deleted_at.fallback=NULL
zero-date.selector=.*
```

Defaults and formats:

- `target.types`: `DATE,DATETIME,TIMESTAMP` by default.
- `fallback.date`: `NULL` or an ISO date `yyyy-MM-dd`.
- `fallback.datetime`: `NULL` or a UTC literal `yyyy-MM-dd HH:mm:ss`.
- `fallback.timestamp`: `NULL` or an ISO-8601 offset datetime such as `1970-01-01T00:00:00Z`.
- `column.<db>.<table>.<column>.fallback`: overrides the type-level value for one column, using the fully qualified column name.

`NULL` promotes the column schema to optional and clears the schema default, so a NOT NULL column can still emit null without being back-filled during Avro serialisation.

Gotcha: a `NULL` fallback promotes the column's Connect schema to optional.

Check: insert a zero-date row in a test table and verify the emitted value.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: converter class and example, target.types, fallback.date/datetime/timestamp formats, per-column override, NULL behaviour.
Removed or reworded: the Avro-compatibility claim.
Method: documentation only; no commands were run.
