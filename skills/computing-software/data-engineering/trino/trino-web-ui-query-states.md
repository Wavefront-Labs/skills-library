---
id: computing-software.data-engineering.trino.trino-web-ui-query-states
name: trino-web-ui-query-states
category: computing-software
field: data-engineering
product: trino
tags: [query-states, blocked-state, query-detail, kill-query, web-ui-overview]
level: practitioner
status: docs-checked
description: "Read the Trino Web UI query list and detail page, interpret QUEUED through FAILED states, and diagnose a persistently BLOCKED query."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/web-interface.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino web ui query states

The Web UI main page lists queries with ID, text, state, percentage complete, user and source. Running queries are on top, followed by recently finished or failed ones.

States:
- `QUEUED`: accepted, awaiting execution.
- `PLANNING`: being planned.
- `STARTING`: execution starting.
- `RUNNING`: at least one task running.
- `BLOCKED`: waiting for resources such as buffer space, memory or splits.
- `FINISHING`: finishing, for example commit for autocommit queries.
- `FINISHED`: done and all output consumed.
- `FAILED`: execution failed.

`BLOCKED` is normal, but a persistent one should be investigated. The docs list the possible causes: insufficient memory or splits, disk or network I/O bottlenecks, data skew where all data goes to a few workers, too little parallelism because few workers are available, or expensive stages that follow. A query is also blocked when the client does not consume results fast enough, which is common with `SELECT *`.

Click a query ID for the detail page: a summary, a graphical view of query stages and a list of tasks, each clickable for task detail. The summary has a button to kill a running query and two visualisations, task execution and timeline. The JSON link shows the full document of query information and statistics. Use these to see where time is spent.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/web-interface.md

Confirmed (page read as raw markdown): the query list columns, all eight states, the BLOCKED causes, and the query detail page contents.
Removed or reworded: the claim that dynamic filter and operator stats appear in the JSON document, which the page does not state.

Method: documentation only; no commands were run.
