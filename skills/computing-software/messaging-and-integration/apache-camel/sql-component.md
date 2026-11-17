---
id: computing-software.messaging-and-integration.apache-camel.sql-component
name: sql-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, sql, jdbc, parameters, polling]
level: practitioner
status: docs-checked
description: "Camel sql component: query as endpoint property, # and :#name parameters, outputType, batch, onConsume hooks, expectedUpdateCount, headers and allowQueryFromHeader risk."
sources:
  - https://camel.apache.org/components/next/sql-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sql:

`sql:query[?options]` (artifact `camel-sql`, uses spring-jdbc). Unlike the JDBC component the query belongs to the endpoint and the payload supplies parameters. Externalise with `sql:classpath:sql/myquery.sql`.

Parameters: positional `#` (`placeholder` option, `usePlaceholder` true). Named `:#name` resolve in order: Simple expressions, Map body, headers, exchange variables; an unresolved name throws. `allowNamedParameters` true; `separator` `,` for String bodies.

Producer: `batch` false (body is an iterator of parameter iterators), `batchAutoCommitDisabled` true, `outputType` `SelectList` (or `SelectOne`, `StreamList`), `noop` false, `useMessageBodyForSql` false (parameters then come from header `CamelSqlParameters`).

Consumer: `onConsume` after each good row (e.g. mark processed), `onConsumeFailed`, `onConsumeBatchComplete` (no parameters), `breakBatchOnConsumeFail` false, `expectedUpdateCount` -1, `useIterator` true, `routeEmptyResultSet` false, `sendEmptyMessageWhenIdle` false, `transacted` false (failure stops and rolls back eagerly).

Headers: `CamelSqlUpdateCount`, `CamelSqlRowCount` (neither set for `StreamList`), `CamelSqlRetrieveGeneratedKeys` (false), `CamelSqlDataSource`.

Security: `allowQueryFromHeader` is false; when true, header `CamelSqlQuery` overrides the query, so enable only for trusted sources.

Verify: a select with `:#id` and a Map body `{id=1}` returns that row as a list of maps.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org sql-component page (URI format and named parameter order, option and header tables via grep, body treatment, batch and result sections).
