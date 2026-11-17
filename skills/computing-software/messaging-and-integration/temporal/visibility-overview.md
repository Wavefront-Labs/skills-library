---
id: computing-software.messaging-and-integration.temporal.visibility-overview
name: visibility-overview
category: computing-software
field: messaging-and-integration
product: temporal
tags: [visibility, visibility-store, count-api, elasticsearch, opensearch, eventual-consistency, describeworkflowexecution]
level: practitioner
status: docs-checked
description: "Temporal Visibility: SQL-like listing and counting of executions, supported stores, eventual consistency, Count API GROUP BY, and when not to rely on it."
sources:
  - https://docs.temporal.io/visibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Visibility is the set of subsystems and APIs for listing, filtering, sorting and counting workflow executions via a SQL-like List Filter, plus custom Search Attributes. The Visibility store is configured as part of persistence. Dual Visibility (server v1.21+) migrates from one store database to another.

Availability: SQL databases (MySQL v8.0.17+, PostgreSQL v12+) with Server v1.20+; Elasticsearch v7+ (Server v1.7+) or v8 (v1.18+); OpenSearch 2+ (Server v1.30.1+). Cloud enables it by default. Standard Visibility was deprecated in v1.21 and removed in v1.24.

Count API: `temporal workflow count -q "WorkflowType='foo'"`; adding `GROUP BY ExecutionStatus` is the only supported grouping and only in Count. Counts are approximate.

Operations reading Visibility (sharing its rate limit and lag): `ListWorkflowExecutions`, `ScanWorkflowExecutions`, `CountWorkflowExecutions`, `ListSchedules`, `CountSchedules`, `ListBatchOperations`, `GetWorkerTaskReachability`, and `DescribeTaskQueue` with reachability. Lookups by ID (`DescribeWorkflowExecution`, `DescribeSchedule`) do not use it.

Freshness: the index is updated asynchronously, so results can be stale for seconds or longer, with no published SLA. For the authoritative state of one execution use `DescribeWorkflowExecution`. Cloud targets 99.5% availability for Visibility reads over a rolling 30 days, a stated objective, not covered by the SLA.

Use it for operational discovery, dashboards and reporting. Do not use it to test existence (start and handle already-started, or describe by ID), to follow progress (use Event History or child workflows), or to coordinate workflows (use signals, updates, children).

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: visibility (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
