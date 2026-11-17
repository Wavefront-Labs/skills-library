---
id: computing-software.data-engineering.trino.trino-resource-group-selectors
name: trino-resource-group-selectors
category: computing-software
field: data-engineering
product: trino
tags: [selector-rules, resource-group-selectors, client-tags, source, group-templates]
level: advanced
status: docs-checked
description: "Route Trino queries to resource groups with selector rules (user, source, queryType, clientTags), dynamic group templates and how clients set source and tags."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/resource-groups.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino resource group selectors

Selectors decide which group a query runs in. All fields inside one selector are ANDed and selectors are checked in order; the first match wins. Patterns use Java regular expressions.

Fields: `user`, `originalUser` (before `SET SESSION AUTHORIZATION`), `authenticatedUser` (the user that actually authenticated), `userGroup` (matched against every group the user belongs to), `source`, `queryText`, `queryType`, `clientTags` (every listed tag must be present) and the required `group`.

`queryType` values include `SELECT`, `EXPLAIN` (not EXPLAIN ANALYZE), `DESCRIBE` (also SHOW), `INSERT` (also CREATE TABLE AS and REFRESH MATERIALIZED VIEW), `UPDATE`, `MERGE`, `DELETE`, `ANALYZE`, `DATA_DEFINITION` and `ALTER_TABLE_EXECUTE`. Route clients that call `system.runtime.kill_query()` through `DATA_DEFINITION` so the kill runs directly instead of queueing behind the query it targets.

Templates build trees dynamically: `${USER}` and `${SOURCE}` expand automatically, and named regex groups such as `jdbc#(?<toolname>.*)` can be used in group names. A query with source `jdbc#powerfulbi`, user `kayla` and tag `hipri` lands in `global.adhoc.bi-powerfulbi.kayla`.

Clients supply selector input:
- CLI: `--source` and `--client-tags`.
- JDBC: connection properties `source` and `clientTags`.

The docs example places `bob` and the `admin` user group in an admin group of 50 concurrent queries, pipeline DDL in `global.data_definition` (5 concurrent), other pipeline work per user under `global.pipeline` (45 total, 5 per user), BI tools at 10 per tool and 3 per user, and everything else in a per-user adhoc group.

## Checked

2026-11-04. Read against the Trino docs page `admin/resource-groups.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
