---
id: computing-software.data-engineering.druid.druid-web-console-overview
name: druid-web-console-overview
category: computing-software
field: data-engineering
product: druid
tags: [web-console, router, query-view, data-loader, datasources]
level: intro
status: docs-checked
description: "Reach the Druid web console through the Router, know what each view does, and the security caveat without permissions."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/web-console.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The web console loads data, manages datasources and tasks, shows server status and segment information, and runs SQL and native queries. It needs the Router's management proxy and Druid SQL on the Brokers, both enabled by default. The Router hosts it: browse to `http://<ROUTER_IP>:<ROUTER_PORT>`.

Security note: without Druid user permissions configured, any API or console user has effectively the same access to local files and network services as the user Druid runs as. Avoid running Druid as root, and use Druid permissions or network firewalls to limit access to sensitive resources.

## Views

- Home: cards for Status (Druid version, loaded extensions), Datasources, Segments, Supervisors, Tasks, Services, Lookups; the data loader and lookups views are reached from the top-level navigation.
- Query: tabbed SQL editor used for SQL-based ingestion and the multi-stage query engine. Features: schema/datasource/column panel; **Connect external data** (samples external data and builds an `EXTERN` query); **Recent query tasks** panel (all users' queries, same as the Tasks view filtered to `type='query_controller'`); **Preview** for INSERT/REPLACE (runs inline without the clause and with an added LIMIT, so results are incomplete); an engine selector (by default picks the endpoint automatically from the query, or choose one and set engine context parameters); **Max tasks** picker for the MSQ-task engine; a More menu (Explain SQL query, Query history, Convert ingestion spec to SQL, Attach tab from task ID, Open query detail archive); live progress and per-stage reports. The original single-query view remains at `#query` in the URL.
- Data loader: step-by-step wizard that builds an ingestion spec with incremental previews. Clicking **Next** fills later steps with defaults; jumping via the top navigation leaves the spec unchanged.
- Datasources: sizes and availability; edit retention rules, configure automatic compaction, drop data; optional segment timeline; **View SQL query for table** for views powered by SQL.
- Segments: all segments, with the ID split into Datasource, Start, End, Version and Partition columns for filtering and sorting.
- Supervisors: status, suspend, resume, reset, **Submit JSON supervisor**, detailed progress reports.
- Tasks: running and recent tasks, grouped by Type, Datasource or Status; **Submit JSON task**; details per task.
- Services: node status, grouped by Type or Tier.
- Lookups: create and edit query-time lookups.

## Checked

2026-11-08. Read the cited web-console page in full. Expanded the draft with per-view functions and the Query view tools.

Method: documentation only; no commands were run.
