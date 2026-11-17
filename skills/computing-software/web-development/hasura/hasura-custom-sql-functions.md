---
id: computing-software.web-development.hasura.hasura-custom-sql-functions
name: hasura-custom-sql-functions
category: computing-software
field: web-development
product: hasura
tags: [hasura, postgres, custom-functions, sql, mutations, queries]
level: advanced
status: docs-checked
description: "Track Postgres user-defined SQL functions as top-level query, subscription or mutation fields, respecting the STABLE VOLATILE return type rules."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/custom-functions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose custom SQL logic as GraphQL root fields.

Constraints from the docs for a trackable function:
- Behavior: `STABLE` or `IMMUTABLE` functions can only be exposed as queries; `VOLATILE` functions can be exposed as mutations or queries.
- Return type: must be `SETOF <table>` or `<table>` where the table is already tracked.
- Argument modes: only `IN`.

Steps:
1. Create the function (Console `Data -> SQL`; the `Track this` checkbox exposes it right away).
2. Track it: Console `Data -> Schema`, the metadata files, or the Metadata API `pg_track_function`.
3. Query it like a field, or subscribe to it when it is a query function.

If the SETOF table does not exist or the function needs a custom row type, the docs suggest creating and tracking an empty table with the required schema to serve as the return type.

A `session_argument` config can be set on `pg_track_function` so a JSON object of session variables is passed to the function (keys are lowercase session variable names).

`VOLATILE` functions can also be tracked under the query root, in which case you must guarantee they do not change the database. Permissions configured on the `SETOF` table apply to the function.

Related: user-defined SQL functions can also be added as computed fields instead.

## Checked

2026-11-04. Confirmed against the cited pages: custom-functions page: volatility rules, return type, IN-only arguments, empty-table workaround, tracking routes, session_argument, VOLATILE under query, SETOF table permissions, computed-field note. Removed or corrected: up.sql/down.sql advice, the multiplexing-errors gotcha and the Verify step (not on the page).

Method: documentation only; no commands were run.
