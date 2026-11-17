---
id: computing-software.messaging-and-integration.apache-camel.jdbc-component
name: jdbc-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, jdbc, sql, producer, datasource]
level: practitioner
status: docs-checked
description: "Camel jdbc component: producer-only, SQL in the body, outputType SelectList default, useHeadersAsParameters with :?name, count headers, generated keys and BLOB handling."
sources:
  - https://camel.apache.org/components/next/jdbc-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jdbc:

Producer only (not usable in `from`). `jdbc:dataSourceName[?options]`, artifact `camel-jdbc`. For Spring transactions use the spring-jdbc component. `dataSourceName` is looked up in the registry; `dataSource` or `default` picks the single DataSource there.

The body is the SQL (text, bytes, stream or file); a message without a body fails with `InvalidPayloadException`. (Contrast the sql component, where the query belongs to the endpoint.)

Options (defaults): `outputType` `SelectList` (also `SelectOne`, `StreamList`), `outputClass`, `readSize` 0, `resetAutoCommit` true (false with XA), `useGetBytesForBlob` false, `useHeadersAsParameters` false, `allowNamedParameters` true, `useJDBC4ColumnNameAndLabelSemantics` true, `lazyStartProducer` false, `parameters` with `statement.` prefix (maxRows, fetchSize).

Named parameters are `:?name` in the SQL; with `useHeadersAsParameters=true` values come from headers (or `CamelJdbcParameters` Map).

Output: default `ArrayList<LinkedHashMap<String, Object>>` keyed by column name. `SelectOne` returns one row Map, a single column value or `null`. `StreamList` is a read-once Iterator. A non-SELECT leaves the body unchanged.

Headers: `CamelJdbcUpdateCount`, `CamelJdbcRowCount` (SelectList), `CamelJdbcColumnNames`, `CamelRetrieveGeneratedKeys` (false), `CamelGeneratedColumns`, `CamelGeneratedKeysRowCount`, `CamelGeneratedKeysRows`.

BLOB/CLOB are readable only while the connection is open: use `useGetBytesForBlob=true` or convert CLOBs to text in SQL. Polling needs a Timer or Quartz.

Verify: a `select` body returns a list of maps and sets `CamelJdbcRowCount`.

## Checked

Method: docs-checked 2026-11-09 against the full camel.apache.org jdbc-component page (component and endpoint options, headers, body and result sections).
