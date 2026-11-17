---
id: computing-software.data-engineering.apache-pinot.apache-pinot-query-quotas-table-database-application
name: apache-pinot-query-quotas-table-database-application
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, query-quota, quota, maxqueriespersecond, databasemaxqueriespersecond, applicationmaxqueriespersecond, applicationname, queryquotaenforcementmode, rate-limiting]
level: practitioner
status: docs-checked
description: "Throttling queries per second at table, database and application level: quota configs, REST calls, enforcement modes, check order."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query quotas

**Table quota**, in the table config. `maxQueriesPerSecond` must be a positive, finite number (zero, negative, NaN and infinity are rejected); omit it for unlimited.
```
"quota": { "maxQueriesPerSecond": 300 }
```
The quota is divided among the active brokers serving the table (300 over 5 brokers is 60 qps each, and a broker fails queries over its share). For a hybrid table, each of OFFLINE and REALTIME has its own quota; a query on the bare table name counts against both and fails if either is reached. A multi-stage query counts against every table it touches.

From 1.7.0, `quota.queryQuotaEnforcementMode` chooses breach handling: `ENFORCED` (default; the query is rejected with 429), `SHADOW` (the `QUERY_QUOTA_EXCEEDED` broker metric and a warning log are recorded, the query still runs), or `DISABLED` (neither metered nor enforced).

**Database quota**: a default for all databases via cluster config, and a per-database override via the controller:
```
POST /cluster/configs        {"databaseMaxQueriesPerSecond": "1000"}
POST /databases/{databaseName}/quotas?maxQueriesPerSecond=1200
GET  /databases/{databaseName}/quotas
```
Split across online brokers like the table quota. A multi-stage query counts toward the database its tables belong to (cross-database queries are not allowed).

**Application quota** (added in 1.3.0): applies by the query's `applicationName` option, for example `SET applicationName='test';`. A non-empty name matching no configured quota falls to the global default; by default neither a global default nor any application quota is set.
```
POST /cluster/configs        {"applicationMaxQueriesPerSecond": "1000"}
GET  /applicationQuotas
POST /applicationQuotas/{applicationName}?maxQueriesPerSecond=1200
```
To disable an application quota, POST with an empty parameter value. Also split across online brokers. The controller Query Console uses the application name `pinot-controller-console` by default, so a quota on that name or a global default can rate-limit console queries.

Order of checks when several apply: application quota, then database quota, then table quota. The query fails at the first limit exceeded; a database breach fails it without reaching the table quota.

## Checked

2026-11-08. Read the whole pinot-docs query-quotas page. Confirmed the three levels, quota value rules, broker splitting, hybrid and multi-stage behaviour, enforcement modes, REST endpoints, check order and application-name behaviour. Corrected the table example (number not string), removed the unsourced "practical use" paragraph and the claim that a rejected query is never queued, and added the 429, shadow and console details.

Method: documentation only; no commands were run.
