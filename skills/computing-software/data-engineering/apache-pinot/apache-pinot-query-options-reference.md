---
id: computing-software.data-engineering.apache-pinot.apache-pinot-query-options-reference
name: apache-pinot-query-options-reference
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, query-options, set, timeoutms, clientqueryid, explainplanverbose, maxexecutionthreads, numgroupslimit, enablenullhandling, numreplicagroupstoquery, usefixedreplica, andrestrictionpushdownmode, sqloptionsmode, validationmode, skipupsert]
level: practitioner
status: docs-checked
description: "Pinot per-query SET options: timeoutMs, numGroupsLimit, maxExecutionThreads, replica selection, null handling and validationMode."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/query-execution-controls/query-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query options reference

Prefix a query with `SET key=value;` statements, or pass them as `queryOptions`.

```
SET timeoutMs=20000;
SET numGroupsLimit=200000;
SELECT country, COUNT(*) FROM t GROUP BY country
```

Common options:
- `useMultistageEngine` - run on the multi-stage engine.
- `timeoutMs` - overall query deadline.
- `clientQueryId` - tag a query so it can be found or cancelled.
- `explainPlanVerbose` - more detail in EXPLAIN output.
- `maxExecutionThreads` - maximum threads used to execute the query.
- `numGroupsLimit` - for group-by queries, caps how many groups an operator keeps before it stops admitting new groups.
- `enableNullHandling` - turn on advanced null semantics for this query.
- `numReplicaGroupsToQuery`, `useFixedReplica` - control replica selection.
- `andRestrictionPushdownMode` - `NEVER` (default), `AUTO` or `ALWAYS`; overrides the server setting.
- `skipUpsert` - read all versions of upserted rows.
- `sqlOptionsMode` - request-level policy for options embedded in SQL: `ALLOW` (default), `IGNORE` or `REJECT`; pass it in REST `queryOptions` or gRPC metadata, not in SQL.

Validation: the cluster setting `pinot.broker.query.option.validationMode` controls unknown keys given through SQL `SET`: the default `NONE` preserves them, `WARN` logs them and `REJECT` fails the query.

## Checked

2026-11-09: confirmed against the Pinot Query options page (pinot-docs build-with-pinot/querying-and-sql/query-execution-controls/query-options.md): the `SET` syntax, the options table entries for each listed option, `andRestrictionPushdownMode` values, `sqlOptionsMode` values and `validationMode` values and default. Reworded `numGroupsLimit`, `maxExecutionThreads` and `validationMode` to match the page.

Method: documentation only; no commands were run.
